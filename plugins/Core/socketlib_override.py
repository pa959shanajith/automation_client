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

import json
import time
import logging
from uuid import uuid4 as uuid
import threading
import requests
from urllib3.connection import HTTPConnection
import socketIO_client
import storage
from socketIO_client.exceptions import *
from socketIO_client.transports import *

log = logging.getLogger("socketio-lib.py")

CHUNK_MAX_LIMIT = 15*1024*1024 # 15 MB
CHUNK_SIZE = 10*1024*1024 # 10 MB
PACKET_TIMEOUT = 60 # Seconds
PAGINATE_INDEX = "p@gIn8"

try:
    store = storage.SQLite()
except:
    store = storage.InMemory()


__all__ = ['SocketIO','BaseNamespace']


class CustomTimer(threading.Thread):
    """ Call a function after a specified number of seconds just like threading.Timer \n
        But this implementation accepts one extra argument called `interval`. \n
        If interval is not passed then default value is assumed to be entire timeout duration. \n
        So, instead of sleeping for entire timeout duration this thread sleep in intervals,
        making it easier to terminate.
    """
    daemon = True
    def __init__(self, timeout=0, callback=lambda *x:x, *args, **kwargs):
        super(CustomTimer, self).__init__()
        self.name = kwargs.pop('name', 'Timer_Thread')
        assert type(timeout) in [int, float], "Timeout Value has to be a floating point number or a integer"
        self.timeout = max(timeout, 0)
        self.timeleft = timeout
        self.chunk = kwargs.pop('interval', timeout)
        assert callable(callback), "callback has to be a callable function"
        if callback is not None and callable(callback):
            self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.terminate = threading.Event()

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

    def run(self):
        while not self.terminate.is_set() and self.timeleft > 0:
            if self.timeleft < self.chunk:
                self.terminate.wait(self.timeleft)
            else:
                self.terminate.wait(self.chunk)
            self.timeleft -= self.chunk
        if not self.terminate.is_set():
            self.callback(*self.args, **self.kwargs)
            self.terminate.set()


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
            kwargs["socket_options"] = HTTPConnection.default_socket_options + self.socket_options
        if self.assert_hostname is not None:
            kwargs["assert_hostname"] = self.assert_hostname
        super(HTTPAdapterWithExtraOptions, self).init_poolmanager(*args, **kwargs)


def socketIO_warn(self, msg, *attrs):
    """ Override SocketIO library's _warn method used for logging. \n
        This is needed because this library doesn't gives anything to stdout or stderr \n
        on exception/warning. Hence Adding custom check and raising exception. Ref #1847.
    """
    self._log(logging.WARNING, msg, *attrs)
    if (("[ssl: certificate_verify_failed]" in msg.lower()) or
        ('certificate verify failed' in msg.lower()) or
        ("hostname" in msg and "doesn't match " in msg)):
        raise ValueError("[Certificate Mismatch] "+ msg)


@property
def socketIO_transport(self):
    """ Override SocketIO library's _transport method used for generating new Transport instance. \n
        This is needed because this library opens new instance after invoking disconnect. Ref #1823.
    """
    if self._opened or self._should_stop_waiting():
        return self._transport_instance
    self._engineIO_session = self._get_engineIO_session()
    self._negotiate_transport()
    self._connect_namespaces()
    self._opened = True
    self._reset_heartbeat()
    return self._transport_instance


@property
def socketIO_waiting_for_close(self):
    """ Add property to SocketIO library to check closing status of socketIO object """
    return self._should_stop_waiting()


def socketIO_close(self):
    """ Override SocketIO library's _close method used for closing a Transport instance.\n
        This is needed because this library never actually closes the connection. \n
        Ref: https://github.com/invisibleroads/socketIO-client/issues/176 \n
        Ref: https://github.com/invisibleroads/socketIO-client/pull/126
    """
    self._wants_to_close = True
    try:
        self._heartbeat_thread.halt()
        self._heartbeat_thread.join()
    except AttributeError:
        pass
    if not hasattr(self, '_opened') or not self._opened:
        self._http_session.close()
        return
    engineIO_packet_type = 1
    try:
        self._transport_instance.send_packet(engineIO_packet_type)
    except (TimeoutError, ConnectionError):
        pass
    self._http_session.close()
    self._transport_instance.close()
    self._opened = False


def socketIO_XHR_close(self):
    """ Add close method in transports.XHR_PollingTransport for closing a Transport instance connection. \n
        This is needed because this library never actually closes the connection. \n
        Ref: https://github.com/invisibleroads/socketIO-client/issues/176 \n
        Ref: https://github.com/invisibleroads/socketIO-client/pull/126
    """
    pass


def socketIO_WS_close(self):
    """ Add close method in transports.WebsocketTransport for closing a Transport instance connection. \n
        This is needed because this library never actually closes the connection. \n
        Ref: https://github.com/invisibleroads/socketIO-client/issues/176 \n
        Ref: https://github.com/invisibleroads/socketIO-client/pull/126
    """
    self._connection.close()


def socketIO_read_packet_length(content, content_index):
    """ Override SocketIO library's parser._read_packet_length method used for reading packets. \n
        This is needed because this library doesn't support Socket.io 2.x \n
        Ref: https://github.com/invisibleroads/socketIO-client/compare/master...nexus-devs:master \n
        Ref: https://github.com/invisibleroads/socketIO-client/pull/158
    """
    start = content_index
    while content.decode()[content_index] != ':':
        content_index += 1
    packet_length_string = content.decode()[start:content_index]
    return content_index, int(packet_length_string)


def socketIO_read_packet_text(content, content_index, packet_length):
    """ Override SocketIO library's parser._read_packet_text method used for reading packets. \n
        This is needed because this library doesn't support Socket.io 2.x \n
        Ref: https://github.com/invisibleroads/socketIO-client/compare/master...nexus-devs:master \n
        Ref: https://github.com/invisibleroads/socketIO-client/pull/158
    """
    while content.decode()[content_index] == ':':
        content_index += 1
    packet_text = content.decode()[content_index:content_index + packet_length]
    return content_index + packet_length, packet_text.encode()


def socketIO_WS_init(self, http_session, is_secure, url, engineIO_session=None):
    """ Override SocketIO library's transports.WebsocketTransport.__init__ method
        used for creating websocket connection. \n
        This is needed because this library doesn't support passing server certificate
    """
    super(WebsocketTransport, self).__init__(
        http_session, is_secure, url, engineIO_session)
    params = dict(http_session.params, **{
        'EIO': ENGINEIO_PROTOCOL, 'transport': 'websocket'})
    request = http_session.prepare_request(requests.Request('GET', url))
    kw = {'header': ['%s: %s' % x for x in request.headers.items()]}
    if engineIO_session:
        params['sid'] = engineIO_session.id
        kw['timeout'] = self._timeout = engineIO_session.ping_timeout
    ws_url = '%s://%s/?%s' % (
        'wss' if is_secure else 'ws', url, format_query(params))
    http_scheme = 'https' if is_secure else 'http'
    if http_scheme in http_session.proxies:  # Use the correct proxy
        proxy_url_pack = parse_url(http_session.proxies[http_scheme])
        kw['http_proxy_host'] = proxy_url_pack.hostname
        kw['http_proxy_port'] = proxy_url_pack.port
        if proxy_url_pack.username:
            kw['http_proxy_auth'] = (
                proxy_url_pack.username, proxy_url_pack.password)
    kw['sslopt'] = {}
    if hasattr(http_session, 'assert_hostname'): # Do not perform hostname check
        kw['sslopt']['check_hostname'] = False
    if http_session.verify:
        kw['sslopt']['cert_reqs'] = ssl.CERT_REQUIRED
        if not isinstance(http_session.verify, bool): kw['sslopt']['ca_certs'] = http_session.verify
        if http_session.cert:  # Specify certificate path on disk
            if isinstance(http_session.cert, six.string_types):
                kw['ca_certs'] = http_session.cert
            else:
                kw['ca_certs'] = http_session.cert[0]
    else:  # Do not verify the SSL certificate
        kw['sslopt']['cert_reqs'] = ssl.CERT_NONE
    try:
        self._connection = create_connection(ws_url, **kw)
    except Exception as e:
        raise ConnectionError(e)


def socketIO_get_response(request, *args, **kw):
    """ Override SocketIO library's transports.get_response method used for processing
        XHR-polling response. This is needed because this library doesn't handle NGINX 504 Error.
    """
    try:
        response = request(*args, stream=True, **kw)
    except requests.exceptions.Timeout as e:
        raise TimeoutError(e)
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(e)
    except requests.exceptions.SSLError as e:
        raise ConnectionError('could not negotiate SSL (%s)' % e)
    status_code = response.status_code
    if 200 != status_code:
        if status_code == 504 and "Avo Assure Error" in response.text: raise ValueError("Avo Assure Server Unavailable")
        raise ConnectionError('unexpected status code (%s %s)' % (
            status_code, response.text))
    return response


def socketIO_prepare_http_session(kw):
    """ Override SocketIO library's transports.prepare_http_session method used for creating
        XHR-polling request. This is needed to provide extra options like disable hostname
        verification or provide additional socket options.
    """
    http_session = prepare_http_session(kw)
    opts = {}
    verify_host = kw.get('assert_hostname', None)
    if verify_host is not None:
        http_session.assert_hostname = opts['assert_hostname'] = verify_host
    # opts['socket_options'] = [(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)]
    http_session.mount('https://', HTTPAdapterWithExtraOptions(**opts))
    http_session.mount('http://', HTTPAdapterWithExtraOptions(**opts))
    return http_session


def socketIO_wait(self, seconds=None, **kw):
    """ Override SocketIO library's wait method used for creating a blocking connection. \n
        This is needed because this library doesn't handle empty packages.
    """
    self._heartbeat_thread.hurry()
    self._heartbeat_thread.setName("socketIO_heartbeat")
    #self._transport.set_timeout(seconds=1)
    #print(self._transport._connection.gettimeout())
    time.sleep(1)
    warning_screen = self._yield_warning_screen(seconds)
    for _ in warning_screen:
        if self._should_stop_waiting(**kw):
            break
        try:
            try:
                self._process_packets()
            except TimeoutError:
                pass
            except KeyboardInterrupt:
                self._close()
                raise
        except ConnectionError as e:
            self._opened = False
            try:
                warning = Exception('[connection error] %s' % e)
                warning_screen.throw(warning)
            except StopIteration:
                self._warn(warning)
            try:
                namespace = self.get_namespace()
                namespace._find_packet_callback('disconnect')()
            except PacketError:
                pass
        except IndexError:  ## New Change
            pass            ## New Change
    self._heartbeat_thread.relax()
    #self._transport.set_timeout()


def socketIO_send(self, data='', callback=None, **kw):
    """ Override SocketIO library's send method used for sending eventless data. \n
        This is needed because this library doesn't pass kwargs to actual emit.
    """
    kw['path'] = kw.get('path', '')
    args = [data]
    if callback:
        args.append(callback)
    self.emit('message', *args, **kw)


def socketIO_on_data_ack(self, pack_id, *args):
    """ Add a ACK_EVENT listener in SocketIO library's socketIO_client.BaseNamespace class \n
        This is needed to free up memory consumed by stored packet, send next packet in queue.
    """
    # log.info("Ack'd "+str(pack_id)+"\tLast_Sent: "+self._io.last_packet_sent)
    # Check if ack recieved matches with the packet sent, Only then process the ACK. Also match id_eof with id
    if (self._io.last_packet_sent != str(pack_id)) and (self._io.last_packet_sent.replace("_eof", '') != str(pack_id)): return None
    if self._io.activeTimer.is_active:
        self._io.activeTimer.cancel()
    # if (self._io.activeTimer != None and self._io.activeTimer.alive):
    #     self._io.activeTimer.cancel()
    #     self._io.activeTimer = None
    # else:
    #     log.error("Timer Fault.\tArg1-"+ str(self._io.activeTimer != None)+"\tArg2-"+str(self._io.activeTimer.is_active))
    idx = pack_id.split('_')
    idx = idx[1] if len(idx) == 2 else None
    if idx == "eof": return None # EOF ACK packets always emit one more ACK. So ignore current one
    if len(args) > 0 and args[0] == "paginate_fail":
        pckt = store.get_packet(int(pack_id.split('_')[0]), "PAGIN")
        self._io.send_pckt(pckt[0], *pckt[1], **pckt[2])
    else:
        store.delete_packet(pack_id)
        if store.has_packet:
            pckt = store.get_packet(store.next_id, idx)
            if pckt: self._io.send_pckt(pckt[0], *pckt[1], **pckt[2])


def socketIO_save_pckt(self, packid, event, *fargs, **fkw):
    """ Helper function to save packets in db/memory before actually sending them. """
    fargs = (packid,) + fargs
    idx = packid.split('_')
    send_now = not store.has_packet
    store.save_packet(int(idx[0]), (idx[1] if len(idx) == 2 else None), [event, fargs, fkw])
    if self.activeTimer.is_inactive:
        if send_now:
            self.send_pckt(event, *fargs, **fkw)
        else:
            pckt = store.get_packet(store.next_id)
            if pckt: self.send_pckt(pckt[0], *pckt[1], **pckt[2])


def socketIO_emit(self, event, *args, **kw):
    """ Override SocketIO library's emit method used for sending data. \n
        This is needed because this library doesn't support packet size larger than 100 MB
    """
    pack_id = store.get_id
    if len(args) == 0 or (len(args) > 0 and type(args[0]) == bool):
        if kw.get('dnack', False):
            self.send_pckt(pack_id, event, *args, **kw)
        else:
            self.save_pckt(pack_id, event, *args, **kw)
    else: # Check for pagination
        payload = args[0]
        stringify = False
        if type(payload) in [dict, list, tuple]:
            stringify = True
            payload = json.dumps(payload)
        size = len(payload)
        # Increasing 45 bytes in check limit (36 bytes for uuid, 2 bytes for separator, 7 bytes for index)
        if not (size > CHUNK_MAX_LIMIT+45): self.save_pckt(pack_id, event, *args, **kw)
        else: # Pagination begins
            sub_pack_id = str(uuid())
            blocks = int(size/CHUNK_SIZE) + 1
            pckt = (';'.join([sub_pack_id,str(size),str(blocks),str(stringify)]))
            self.save_pckt(pack_id+"_"+PAGINATE_INDEX, event, pckt, **kw)
            for i in range(blocks):
                pckt = (sub_pack_id+';'+payload[CHUNK_SIZE*i : CHUNK_SIZE*(i+1)])
                self.save_pckt(pack_id+'_'+str(i+1), event, pckt, **kw)
            self.save_pckt(pack_id+"_eof", event, sub_pack_id, **kw)
            del payload


def socketIO_send_pckt(self, event, *args, **kw):
    """ Helper function to start timer before actually send packets. """
    pktid = str(args[0])
    # log.info("Sending: "+ pktid + "\tThread Alive: "+str(self.activeTimer.is_active))
    if not kw.get('dnack', False):
        self.last_packet_sent = pktid
        self.activeTimer = CustomTimer(PACKET_TIMEOUT, self.send_pckt, event, *args, interval=2, name="packet#"+str(args[0])+"_timeout", **kw)
        self.activeTimer.start()
    try:
        self._emit(event, *args, **kw)
    except Exception as e:
        log.debug("Error while sending packet with id:"+pktid+", Error:", e)
    del args


socketIO_client.parsers._read_packet_length = socketIO_read_packet_length
socketIO_client.parsers._read_packet_text = socketIO_read_packet_text
socketIO_client.transports.get_response = socketIO_get_response
socketIO_client.transports._prepare_http_session = socketIO_client.transports.prepare_http_session
socketIO_client.prepare_http_session = socketIO_client.transports.prepare_http_session = socketIO_prepare_http_session
socketIO_client.XHR_PollingTransport.close = socketIO_XHR_close
socketIO_client.WebsocketTransport.__init__ = socketIO_WS_init
socketIO_client.WebsocketTransport.close = socketIO_WS_close
socketIO_client.BaseNamespace.on_data_ack = socketIO_on_data_ack
socketIO_client.SocketIO.save_pckt = socketIO_save_pckt
socketIO_client.SocketIO.send_pckt = socketIO_send_pckt
socketIO_client.SocketIO._emit = socketIO_client.SocketIO.emit
socketIO_client.SocketIO.emit = socketIO_emit
socketIO_client.SocketIO._send = socketIO_client.SocketIO.send
socketIO_client.SocketIO.send = socketIO_send
socketIO_client.SocketIO._warn = socketIO_warn
socketIO_client.SocketIO._close = socketIO_close
socketIO_client.SocketIO._transport = socketIO_transport
socketIO_client.SocketIO.waiting_for_close = socketIO_waiting_for_close
socketIO_client.SocketIO.wait = socketIO_wait
socketIO_client.SocketIO.activeTimer = CustomTimer()
socketIO_client.SocketIO.last_packet_sent = None

SocketIO = socketIO_client.SocketIO
BaseNamespace = socketIO_client.BaseNamespace