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
import json
import logging
import requests
import urllib3
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
except:
    store = storage.InMemory()

__all__ = ['SocketIO','BaseNamespace','prepare_http_session']


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


class EngineIO(EioClient):
    """ Wrapper class for engineio.Client \n
        This is needed because this library doesn't have provide exception for
        http requests. Also, websocket connection does not work with
        self-signed certificate or hostname mismatch.
    """
    def __init__(self, *args, **kwargs):
        self.hidden_error = None
        self.parent = super(EngineIO, self)
        self.__connect_websocket = self.parent._connect_websocket
        self.parent.__init__(*args, **kwargs)

    def _send_request(self, method, url, headers=None, body=None, timeout=None):  # pragma: no cover
        if self.http is None:
            self.http = requests.Session()
        try:
            return self.http.request(method, url, headers=headers, data=body,
                timeout=timeout, verify=self.ssl_verify)
        except requests.exceptions.RequestException as exc:
            self.logger.info('HTTP %s request to %s failed with error %s.',
                method, url, exc)
            self.hidden_error = exc   ##~

    def _connect_websocket(self, url, headers, engineio_path):
        """Establish or upgrade to a WebSocket connection with the server."""
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
        extra_options['sslopt'] = {}   ##~
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
    """ Wrapper class for requests.adapters.HTTPAdapter \n
        This is needed because this library doesn't have option to provide
        socket_options or other kwargs to pass to pool manager.
    """
    def __init__(self, *args, **kwargs):
        self.parent = super(SocketIO, self)
        self.user_callbacks = {}
        self.parent.__init__(*args, **kwargs)

    def _wip_emit(self, event, data=None, namespace=None, callback=None, **kw):
        pktid = store.id
        if not data or type(data) == bool:
            self._save_packet(pktid, event, data, **kw)
        else: # Check for pagination
            stringify = False
            if type(data) in [dict, list, tuple]:
                stringify = True
                data = json.dumps(data)
            data_size = len(data)
            # Increasing 45 bytes in check limit (36 bytes for uuid,
            #     2 bytes for separator, 7 bytes for index)
            if not (data_size > CHUNK_MAX_SIZE+45):
                self._save_packet(pktid, event, data, **kw)
            else: # Pagination begins
                sub_pack_id = str(uuid())
                blocks = int(data_size/CHUNK_SIZE) + 1
                pckt = (';'.join([sub_pack_id,str(data_size),str(blocks),str(stringify)]))
                self._save_packet(pktid+"_"+PAGINATE_INDEX, event, pckt, **kw)
                for i in range(blocks):
                    pckt = (sub_pack_id+';'+data[CHUNK_SIZE*i : CHUNK_SIZE*(i+1)])
                    self._save_packet(pktid+'_'+str(i+1), event, pckt, **kw)
                self._save_packet(pktid+"_eof", event, sub_pack_id, **kw)
                del data

        if callback is not None:
            self.user_callbacks[pktid] = callback
        self.parent.emit(event, data, namespace, self._ack_callback)

    def emit(self, event, data=None, namespace=None, callback=None, **kw):
        self.parent.emit(event, data, namespace, callback)

    def send(self, data, namespace=None, callback=None, **kw):
        self.emit('message', data=data, namespace=namespace,
                  callback=callback, **kw)

    def _save_packet(self, pktid, event, data, **kw):
        pass

    def _ack_callback(self, id, *args):
        # print(id, args)
        ## ACK Logic

        callback = None
        try:
            callback = self.user_callbacks[id]
        except KeyError:
            log.warning('Unknown callback request received, ignoring.')
        else:
            del self.user_callbacks[id]
        if callback is not None:
            try:
                callback()
            except TypeError:
                log.warning('Acknowledgement callbacks do not support' +
                 'arguments. Callback ignored')

    def _engineio_client_class(self):
        return EngineIO


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
