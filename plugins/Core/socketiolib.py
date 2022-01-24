#-------------------------------------------------------------------------------
# Name:        socketlib_override
# Purpose:     Override SocketIO library's internal methods to deal with
#              application specific issues
#
# Author:      ranjan.agrawal
#
# Created:     03-10-2018
# Copyright:   (c) ranjan.agrawal 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import ssl
import json
import logging
import urllib3
import requests
import threading
import socketio
from engineio.client import websocket, b64encode, ssl, six, urllib, exceptions, packet, connected_clients, Client as EioClient
from uuid import uuid4 as uuid
import storage

logging.getLogger('socketio.client').setLevel(logging.WARN)
logging.getLogger('engineio.client').setLevel(logging.WARN)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
log = logging.getLogger("socketiolib.py")

BaseNamespace = socketio.namespace.ClientNamespace
HTTP_MAX_RETRIES = int(os.getenv('HTTP_MAX_RETRIES', 0))
PAGINATE_INDEX = os.environ['ICE_PACKET_PAGINATE_INDEX'] = "p@gIn8"
PACKET_TIMEOUT = int(os.getenv('ICE_PACKET_TIMEOUT', 60)) # Seconds
CHUNK_MAX_SIZE = int(os.getenv('PACKET_CHUNK_MAX_SIZE', 15))*1024*1024 # 15 MB
CHUNK_SIZE = int(os.getenv('PACKET_CHUNK_SIZE', 10))*1024*1024 # 10 MB

try:
    store = storage.SQLite()
except Exception as e:
    log.error("Unable to use dbstore for packets. Error: %s", e)
    store = storage.InMemory()

__all__ = ['SocketIO','BaseNamespace','prepare_http_session']


class CustomTimer(threading.Thread):
    """ Call a function after a specified number of seconds similar to
    threading.Timer
    
    But this implementation accepts one extra argument called `interval`
    
    If interval is not passed then default value is assumed to be entire
    timeout duration.
    
    So, instead of sleeping for entire timeout duration this thread sleep
    in intervals, making it easier to terminate.
    """
    daemon = True
    def __init__(self, timeout=0, callback=lambda *x:x, *args, **kwargs):
        super(CustomTimer, self).__init__()
        self.name = kwargs.pop('name', 'Timer_Thread')
        assert type(timeout) in [int, float], ("Timeout Value has to be a" +
            "floating point number or a integer")
        self.timeout = max(timeout, 0)
        self.timeleft = timeout
        self.chunk = kwargs.pop('interval', timeout)
        assert callable(callback), "callback has to be a callable function"
        if callback is not None and callable(callback):
            self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.terminate = threading.Event()
        self.awake = threading.Event()

    @property
    def is_cancelled(self):
        return self.terminate.is_set()

    @property
    def is_active(self):
        return self.is_alive() and not self.is_cancelled

    @property
    def is_inactive(self):
        return not self.is_active

    def cancel(self):
        self.terminate.set()

    def resume(self):
        self.awake.set()

    def run(self):
        while (not self.terminate.is_set() and self.timeleft > 0 and 
          not self.awake.is_set()):
            if self.timeleft < self.chunk:
                self.terminate.wait(self.timeleft)
            else:
                self.terminate.wait(self.chunk)
            self.timeleft -= self.chunk
        if not self.terminate.is_set():
            self.callback(*self.args, **self.kwargs)
            self.terminate.set()


class EngineIO(EioClient):
    """ Wrapper class for engineio.Client \n
        This is needed because this library doesn't have provide exception for
        http requests. Also, websocket connection does not work with
        self-signed certificate or hostname mismatch.

        Methods overridden are _send_request and _connect_websocket
    """
    def __init__(self, *args, **kwargs):
        self.hidden_error = None
        self.parent = super(EngineIO, self)
        self.__connect_websocket = self.parent._connect_websocket
        self.parent.__init__(*args, **kwargs)

    def _send_request(self, method, url, headers=None, body=None, timeout=None):  # pragma: no cover
        """Send HTTP request to server.

        Overridden library's send_request method, as it doesn't provide
        the actual error to process/relay forward.
        """
        if self.http is None:
            self.http = requests.Session()
        try:
            return self.http.request(method, url, headers=headers, data=body,
                timeout=timeout, verify=self.ssl_verify, proxies=self.http.proxies)
        except requests.exceptions.RequestException as exc:
            self.logger.info('HTTP %s request to %s failed with error %s.',
                method, url, exc)
            self.hidden_error = exc   ##~

    def _connect_websocket(self, url, headers, engineio_path):
        """Establish or upgrade to a WebSocket connection with the server.
        
        This method is overrriden because library doesn't support custom tls
        options like enable/disable hostname check while connection or
        provide custom CA bundle for connection.
        """
        if websocket is None:  # pragma: no cover
            # not installed
            self.logger.warning('websocket-client package not installed, only '
                                'polling transport is available')
            return False
        websocket_url = self._get_engineio_url(url, engineio_path, 'websocket')
        if self.sid:
            self.logger.info(
                'Attempting WebSocket upgrade to ' + websocket_url)
            upgrade = True
            websocket_url += '&sid=' + self.sid
        else:
            upgrade = False
            self.base_url = websocket_url
            self.logger.info(
                'Attempting WebSocket connection to ' + websocket_url)

        # get cookies and other settings from the long-polling connection
        # so that they are preserved when connecting to the WebSocket route
        cookies = None
        extra_options = {}
        # extra_options['sslopt'] = {}   ##~
        extra_options['sslopt'] = {'ssl_version': ssl.PROTOCOL_TLSv1_2}   ##~
        if self.http:
            # cookies
            cookies = '; '.join(["{}={}".format(cookie.name, cookie.value)
                                    for cookie in self.http.cookies])
            for header, value in headers.items():
                if header.lower() == 'cookie':
                    if cookies:
                        cookies += '; '
                    cookies += value
                    del headers[header]
                    break

            # auth
            if 'Authorization' not in headers and self.http.auth is not None:
                if not isinstance(self.http.auth, tuple):  # pragma: no cover
                    raise ValueError('Only basic authentication is supported')
                basic_auth = '{}:{}'.format(
                    self.http.auth[0], self.http.auth[1]).encode('utf-8')
                basic_auth = b64encode(basic_auth).decode('utf-8')
                headers['Authorization'] = 'Basic ' + basic_auth

            # cert
            # this can be given as ('certfile', 'keyfile') or just 'certfile'
            if isinstance(self.http.cert, tuple):
                extra_options['sslopt']['certfile'] = self.http.cert[0]   ##~
                extra_options['sslopt']['keyfile'] = self.http.cert[1]   ##~
            elif self.http.cert:
                extra_options['sslopt']['certfile'] = self.http.cert   ##~

            # proxies
            if self.http.proxies:
                proxy_url = None
                if websocket_url.startswith('ws://'):
                    proxy_url = self.http.proxies.get(
                        'ws', self.http.proxies.get('http'))
                else:  # wss://
                    proxy_url = self.http.proxies.get(
                        'wss', self.http.proxies.get('https'))
                if proxy_url:
                    parsed_url = urllib.parse.urlparse(
                        proxy_url if '://' in proxy_url
                        else 'scheme://' + proxy_url)
                    # print(parsed_url)   ##~
                    extra_options['http_proxy_host'] = parsed_url.hostname
                    extra_options['http_proxy_port'] = parsed_url.port
                    extra_options['http_proxy_auth'] = (
                        (parsed_url.username, parsed_url.password)
                        if parsed_url.username or parsed_url.password
                        else None)

            # verify
            if not self.http.verify:
                self.ssl_verify = False

            if hasattr(self.http, 'assert_hostname'): # Do not perform hostname check   ##~
                extra_options['sslopt']['check_hostname'] = False   ##~

        if not self.ssl_verify:
            extra_options['sslopt'] = {"cert_reqs": ssl.CERT_NONE}
        else:   ##~
            extra_options['sslopt']['cert_reqs'] = ssl.CERT_REQUIRED   ##~
            if not isinstance(self.ssl_verify, bool):   ##~
                extra_options['sslopt']['ca_certs'] = self.ssl_verify   ##~

        try:
            ws = websocket.create_connection(
                websocket_url + self._get_url_timestamp(), header=headers,
                cookie=cookies, enable_multithread=True, **extra_options)
        except (ConnectionError, IOError, websocket.WebSocketException) as e:   ##~
            self.logger.error('WebSocket upgrade failed: error: %s', str(e))   ##~
            if upgrade:
                self.logger.warning(
                    'WebSocket upgrade failed: connection error')
                return False
            else:
                raise exceptions.ConnectionError('Connection error')
        if upgrade:
            p = packet.Packet(packet.PING,
                                data=six.text_type('probe')).encode()
            try:
                ws.send(p)
            except Exception as e:  # pragma: no cover
                self.logger.warning(
                    'WebSocket upgrade failed: unexpected send exception: %s',
                    str(e))
                return False
            try:
                p = ws.recv()
            except Exception as e:  # pragma: no cover
                self.logger.warning(
                    'WebSocket upgrade failed: unexpected recv exception: %s',
                    str(e))
                return False
            pkt = packet.Packet(encoded_packet=p)
            if pkt.packet_type != packet.PONG or pkt.data != 'probe':
                self.logger.warning(
                    'WebSocket upgrade failed: no PONG packet')
                return False
            p = packet.Packet(packet.UPGRADE).encode()
            try:
                ws.send(p)
            except Exception as e:  # pragma: no cover
                self.logger.warning(
                    'WebSocket upgrade failed: unexpected send exception: %s',
                    str(e))
                return False
            self.current_transport = 'websocket'
            self.logger.info('WebSocket upgrade was successful')
        else:
            try:
                p = ws.recv()
            except Exception as e:  # pragma: no cover
                raise exceptions.ConnectionError(
                    'Unexpected recv exception: ' + str(e))
            open_packet = packet.Packet(encoded_packet=p)
            if open_packet.packet_type != packet.OPEN:
                raise exceptions.ConnectionError('no OPEN packet')
            self.logger.info(
                'WebSocket connection accepted with ' + str(open_packet.data))
            self.sid = open_packet.data['sid']
            self.upgrades = open_packet.data['upgrades']
            self.ping_interval = int(open_packet.data['pingInterval']) / 1000.0
            self.ping_timeout = int(open_packet.data['pingTimeout']) / 1000.0
            self.current_transport = 'websocket'

            self.state = 'connected'
            connected_clients.append(self)
            self._trigger_event('connect', run_async=False)
        self.ws = ws

        # start background tasks associated with this client
        self.ping_loop_task = self.start_background_task(self._ping_loop)
        self.write_loop_task = self.start_background_task(self._write_loop)
        self.read_loop_task = self.start_background_task(
            self._read_loop_websocket)
        return True


class SocketIO(socketio.Client):
    """ Wrapper class for socketio.Client \n

        We have overridden the emit and send method to save packets
        before sending.
        Also, to take the changes in engineio.Client class instance
    """
    def __init__(self, *args, **kwargs):
        self.parent = super(SocketIO, self)
        self.user_callbacks = {}
        self.last_packet_sent = ""
        self.timer = self._timer_class()
        self.emitlock = threading.Lock()
        self.parent.__init__(*args, **kwargs)

    def emit(self, event, data=None, namespace=None, callback=None, **kw):
        """Emit a custom event to one or more connected client namespace

        This method is wrapper for library's emit method. This is done because
        we need to store packets in store before sending it to server.
        """
        packetid = store.id

        # Send packets that do not require acknowledgement immediately
        if kw.pop('dnack', False):
            return self.parent.emit(event, (packetid, data), namespace, callback)

        self._save_packet(packetid, event, namespace, data)

        if callback is not None:
            self.user_callbacks[packetid] = callback

        # Check if transmission is already in progress, if yes, then return
        if self.timer.is_active: return
        self._fetch_n_emit()

    def _fetch_n_emit(self):
        """Fetches next packet from store and invokes _emit to send packet """
        with self.emitlock:
            if self.timer.is_active: return
            _, _, packet = store.load()
            if packet:
                event, namespace, data = packet
                self._emit(event, data, namespace)

    def _emit(self, event, data=None, namespace=None, **kw):
        """Sends the packet to server """
        if store.type == 'db': data = tuple(data)
        self.last_packet_sent = pktid = data[0]
        # log.info("Sending: %s\tThread Alive: %s",pktid,self.timer.is_active)
        self.timer = self._timer_class(PACKET_TIMEOUT, self._emit, event, data,
            namespace, interval=2, name="packet#"+pktid+"_timeout")
        self.timer.start()
        self.parent.emit(event, data, namespace, self._ack_callback)

    def send(self, data, namespace=None, callback=None, **kw):
        """Sends a message to one or more connected client namespace

        This method is wrapper for library's send method. This was needed
        because library does not support kwargs
        """
        self.emit('message', data=data, namespace=namespace,
                  callback=callback, **kw)

    def safe_disconnect(self):
        """Disconnects socketio client from server
        
        If there is an active transmission, then we need to resend it
        
        So, packet being transmitted before disconnect is re-added to queue
        """
        self.disconnect()
        if self.timer.is_inactive: return

        # Since a timer was running that means a packet was being sent. So,
        #   that packet has to be re-added at top of the queue. If packet being
        #   sent was paginated then all previous ids also has to be added
        self.timer.cancel()
        pktid = self.timer.args[1][0] # args[1] is data and data[0] is pktid
        self._re_add_failed_packets(pktid)

    def _re_add_failed_packets(self, pktid):
        """Return a list of packets that needs to be added to the queue if
        last transmission failed. May return multiple values if paginated
        packet was being transmitted
        """
        pktids = []
        if len(pktid.split('_')) == 1: pktids.append(pktid)
        else:
            mpktid, chunkid = pktid.split('_')
            if chunkid == PAGINATE_INDEX: pktids.append(pktid)
            else:
                pktids.append(mpktid+'_'+PAGINATE_INDEX)
                addtill = chunkid
                if chunkid == 'eof':
                    # Get number of packets main packet was broken into
                    start_packet = store.load_packet(mpktid, PAGINATE_INDEX)
                    if start_packet:
                        addtill = start_packet[2][1].split(';')[2]
                    else:
                        # Header packet not found. Remove entire packet
                        addtill = 0
                        store.delete(mpktid)
                for i in range(1, int(addtill)+1):
                    pktids.append(mpktid+'_'+str(i))
                if chunkid == 'eof':
                    # if addtill is 0 then header packet of paginated data was
                    #    not found. Ignore corrupt packet
                    if addtill: pktids.append(pktid)
                    else: del pktids[:]
        store.re_add_ids(pktids)

    def _save_packet(self, pktid, event, nsp, data):
        """Saves the packet to store before transmitting

        If packet size exceeds set limit, then packet is broken down to chunks
        and send separately and recombined in server.
        """
        if not data or type(data) == bool:
            return store.save(pktid, None, [event, nsp, (pktid, data)])

        # Check for pagination
        stringify = False
        payload = data
        if type(data) in [dict, list, tuple]:
            stringify = True
            payload = json.dumps(payload)
        payload_size = len(payload)

        # Increasing 45 bytes in check limit (36 bytes for uuid,
        #   2 bytes for separator, 7 bytes for index)
        if not (payload_size > CHUNK_MAX_SIZE+45):
            return store.save(pktid, None, [event, nsp, (pktid, data)])

        # Pagination begins
        sub_pack_id = str(uuid())
        blocks = int(payload_size/CHUNK_SIZE) + 1
        pckt = (';'.join([sub_pack_id,str(payload_size),str(blocks),str(stringify)]))
        store.save(pktid, PAGINATE_INDEX, [event, nsp, (pktid+'_'+PAGINATE_INDEX, pckt)])
        for i in range(blocks):
            ci = str(i+1)
            pckt = (sub_pack_id+';'+payload[CHUNK_SIZE*i : CHUNK_SIZE*(i+1)])
            store.save(pktid, ci, [event, nsp, (pktid+'_'+ci, pckt)])
        store.save(pktid, "eof", [event, nsp, (pktid+"_eof", sub_pack_id)])
        del data

    def _ack_callback(self, pktid, *args):
        """Acknowledgement received from server to indicate packet sent from
        client is received

        If there are other packets in queue, then next packet in queue is sent
        """
        # log.info("Ack'd: %s\tLast_Sent: %s", pktid, self.last_packet_sent)
        # Check if ack recieved matches with the packet sent, Only then process
        #   the ACK.
        if self.last_packet_sent != str(pktid): return None
        if self.timer.is_active:
            self.timer.cancel()

        # Since ACK is received, mark the queue item as done.
        store.process_done()
        idx = pktid.split('_')
        pktid = idx[0]
        idx = idx[1] if len(idx) == 2 else None
        if len(args) > 0 and args[0] == "paginate_fail":
            self._re_add_failed_packets(pktid+'_eof')
        else:
            if idx is None or idx == "eof":
                store.delete(pktid)
            if store.has_packet:
                self._fetch_n_emit()
                #  and not self.emitlock.locked():

        callback = None
        try:
            callback = self.user_callbacks[pktid]
        except KeyError:
            pass
        else:
            del self.user_callbacks[pktid]
        if callback is not None:
            try:
                callback()
            except TypeError:
                log.warning('Acknowledgement callbacks do not support' +
                 'arguments. Callback ignored')

    def _engineio_client_class(self):
        return EngineIO

    @property
    def _timer_class(self):
        return CustomTimer


class HTTPAdapterWithExtraOptions(requests.adapters.HTTPAdapter):
    """ Wrapper class for requests.adapters.HTTPAdapter \n
        This is needed because this library doesn't have option to provide
        socket_options or other kwargs to pass to pool manager.
    """
    def __init__(self, *args, **kwargs):
        self.socket_options = kwargs.pop("socket_options", None)
        self.assert_hostname = kwargs.pop("assert_hostname", None)
        super(HTTPAdapterWithExtraOptions, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        if self.socket_options is not None:
            if isinstance(self.socket_options, tuple):
                self.socket_options = [self.socket_options]
            kwargs["socket_options"] = urllib3.connection.HTTPConnection.default_socket_options + self.socket_options
        if self.assert_hostname is not None:
            kwargs["assert_hostname"] = self.assert_hostname
        super(HTTPAdapterWithExtraOptions, self).init_poolmanager(*args, **kwargs)


def prepare_http_session(kw):
    """ Generate requests.session object based on provided keyword arguments
    """
    cert = kw.get('cert')
    opts = {}
    verify_host = kw.get('assert_hostname', None)
    http_session = requests.Session()
    http_session.headers.update(kw.get('headers', {}))
    http_session.auth = kw.get('auth')
    http_session.proxies.update(kw.get('proxies', {}))
    http_session.hooks.update(kw.get('hooks', {}))
    http_session.params.update(kw.get('params', {}))
    http_session.verify = kw.get('verify', True)
    http_session.cert = None if (hasattr(cert, '__iter__') and cert[0] is None) else cert
    http_session.cookies.update(kw.get('cookies', {}))
    if verify_host is not None:
        http_session.assert_hostname = opts['assert_hostname'] = verify_host
    if HTTP_MAX_RETRIES: opts['max_retries'] = HTTP_MAX_RETRIES
    # opts['socket_options'] = [(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)]
    http_session.mount('https://', HTTPAdapterWithExtraOptions(**opts))
    http_session.mount('http://', HTTPAdapterWithExtraOptions(**opts))
    return http_session
