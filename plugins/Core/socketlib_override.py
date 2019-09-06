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
import socketIO_client
from uuid import uuid4 as uuid
from socketIO_client.exceptions import *
from socketIO_client.transports import *

CHUNK_MAX_LIMIT = 15*1024*1024 # 15 MB
CHUNK_SIZE = 10*1024*1024 # 10 MB

__all__ = ['SocketIO','BaseNamespace']

""" Override SocketIO library's _warn method used for logging.
    This is needed because this library doesn't gives anything to stdout or stderr
    on exception/warning. Hence Adding custom check and raising exception. Ref #1847.
"""
def socketIO_warn(self, msg, *attrs):
    self._log(logging.WARNING, msg, *attrs)
    if ("[SSL: CERTIFICATE_VERIFY_FAILED]" in msg) or ("hostname" in msg and "doesn't match " in msg):
        raise ValueError("[Certificate Mismatch] "+ msg)

""" Override SocketIO library's _transport method used for generating new Transport instance.
    This is needed because this library opens new instance after invoking disconnect. Ref #1823.
"""
@property
def socketIO_transport(self):
    if self._opened or self._should_stop_waiting():
        return self._transport_instance
    self._engineIO_session = self._get_engineIO_session()
    self._negotiate_transport()
    self._connect_namespaces()
    self._opened = True
    self._reset_heartbeat()
    return self._transport_instance

""" Add property to SocketIO library to check closing status of socketIO object """
@property
def socketIO_waiting_for_close(self):
    return self._should_stop_waiting()

""" Override SocketIO library's _close method used for closing a Transport instance.
    This is needed because this library never actually closes the connection.
    Ref: https://github.com/invisibleroads/socketIO-client/issues/176
    Ref: https://github.com/invisibleroads/socketIO-client/pull/126
"""
def socketIO_close(self):
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

""" Add close method in transports.XHR_PollingTransport for closing a Transport instance connection.
    This is needed because this library never actually closes the connection.
    Ref: https://github.com/invisibleroads/socketIO-client/issues/176
    Ref: https://github.com/invisibleroads/socketIO-client/pull/126
"""
def socketIO_XHR_close(self):
    pass

""" Add close method in transports.WebsocketTransport for closing a Transport instance connection.
    This is needed because this library never actually closes the connection.
    Ref: https://github.com/invisibleroads/socketIO-client/issues/176
    Ref: https://github.com/invisibleroads/socketIO-client/pull/126
"""
def socketIO_WS_close(self):
    self._connection.close()

""" Override SocketIO library's parser._read_packet_length method used for reading packets.
    This is needed because this library doesn't support Socket.io 2.x
    Ref: https://github.com/invisibleroads/socketIO-client/compare/master...nexus-devs:master
    Ref: https://github.com/invisibleroads/socketIO-client/pull/158
"""
def socketIO_read_packet_length(content, content_index):
    start = content_index
    while content.decode()[content_index] != ':':
        content_index += 1
    packet_length_string = content.decode()[start:content_index]
    return content_index, int(packet_length_string)

""" Override SocketIO library's parser._read_packet_text method used for reading packets.
    This is needed because this library doesn't support Socket.io 2.x
    Ref: https://github.com/invisibleroads/socketIO-client/compare/master...nexus-devs:master
    Ref: https://github.com/invisibleroads/socketIO-client/pull/158
"""
def socketIO_read_packet_text(content, content_index, packet_length):
    while content.decode()[content_index] == ':':
        content_index += 1
    packet_text = content.decode()[content_index:content_index + packet_length]
    return content_index + packet_length, packet_text.encode()

""" Override SocketIO library's transports.WebsocketTransport.__init__ method
    used for creating websocket connection.
    This is needed because this library doesn't support passing server certificate
"""
def socketIO_WS_init(self, http_session, is_secure, url, engineIO_session=None):
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
    if http_session.verify:
        kw['sslopt'] = {'cert_reqs': ssl.CERT_REQUIRED, 'ca_certs': http_session.verify, 'check_hostname': False}  ## New Change
        if http_session.cert:  # Specify certificate path on disk
            if isinstance(http_session.cert, six.string_types):
                kw['ca_certs'] = http_session.cert
            else:
                kw['ca_certs'] = http_session.cert[0]
    else:  # Do not verify the SSL certificate
        kw['sslopt'] = {'cert_reqs': ssl.CERT_NONE}
    try:
        self._connection = create_connection(ws_url, **kw)
    except Exception as e:
        raise ConnectionError(e)

""" Override SocketIO library's wait method used for creating a blocking connection.
    This is needed because this library doesn't handle empty packages.
"""
def socketIO_wait(self, seconds=None, **kw):
    self._heartbeat_thread.hurry()
    #self._transport.set_timeout(seconds=1)
    warning_screen = self._yield_warning_screen(seconds)
    for elapsed_time in warning_screen:
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

""" Add a ACK_EVENT listener in SocketIO library's socketIO_client.BaseNamespace class
    This is needed to free up memory consumed by stored packet.
"""
def socketIO_on_data_ack(self, pack_id, *args):
    self._io.emitting = False
    if (pack_id in self._io.evdata): del self._io.evdata[pack_id]


""" Add a NACK_EVENT listener in SocketIO library's socketIO_client.BaseNamespace class
    This is needed to resend lost chunks of stored packet.
"""
def socketIO_on_data_nack(self, pack_id, indexes, *args):
    packet = self._io.evdata[pack_id]
    ev = packet['e']
    kw = packet['kw']
    if indexes == "all": indexes = range(1,packet['b']+1)
    for i in indexes:
        self._io.emit(ev, packet['d'][i], enable_loop=False,**kw)
    return self._io.emit(ev, pack_id+";eof", enable_loop=False, **kw)

""" Override SocketIO library's emit method used for sending data.
    This is needed because this library doesn't support packet size largen than 100 MB
"""
def socketIO_emit(self, event, *args, **kw):
    enable_loop = kw.pop('enable_loop', True)
    while self.emitting and enable_loop:
        time.sleep(1)
    if len(args) == 0 or (len(args) > 0 and type(args[0]) == bool): return self._emit(event, *args, **kw)
    payload = args[0]
    stringify = False
    if type(payload) in [dict, list, tuple]:
        stringify = True
        payload = json.dumps(payload)
    size = len(payload)
    # Increasing 45 bytes (36 bytes for uuid, 2 bytes for separator, 7 bytes for index)
    if not (size > CHUNK_MAX_LIMIT+45): return self._emit(event, *args, **kw)
    else:
        self.emitting = True
        pack_id = str(uuid())
        data = []
        blocks = int(size/CHUNK_SIZE) + 1
        data.append(';'.join([pack_id,"p@gIn8",str(size),str(blocks),str(stringify)]))
        for i in range(blocks):
            data.append(pack_id+';'+str(i+1)+';'+payload[CHUNK_SIZE*i : CHUNK_SIZE*(i+1)])
        del payload
        self.evdata[pack_id] = {'e': event, 'b': blocks, 'd': data, 'kw': kw}
        return self._emit(event, data[0], **kw)

##def socketIO_on_event(self, data_parsed, namespace):
##    self._custom_on_event(data_parsed, namespace)


socketIO_client.parsers._read_packet_length = socketIO_read_packet_length
socketIO_client.parsers._read_packet_text = socketIO_read_packet_text
socketIO_client.XHR_PollingTransport.close = socketIO_XHR_close
socketIO_client.WebsocketTransport.__init__ = socketIO_WS_init
socketIO_client.WebsocketTransport.close = socketIO_WS_close
socketIO_client.BaseNamespace.on_data_ack = socketIO_on_data_ack
socketIO_client.BaseNamespace.on_data_nack = socketIO_on_data_nack
socketIO_client.SocketIO._emit = socketIO_client.SocketIO.emit
socketIO_client.SocketIO.emit = socketIO_emit
#socketIO_client.SocketIO._custom_on_event = socketIO_client.SocketIO._on_event
#socketIO_client.SocketIO._on_event = socketIO_on_event
socketIO_client.SocketIO._warn = socketIO_warn
socketIO_client.SocketIO._close = socketIO_close
socketIO_client.SocketIO._transport = socketIO_transport
socketIO_client.SocketIO.waiting_for_close = socketIO_waiting_for_close
socketIO_client.SocketIO.wait = socketIO_wait
socketIO_client.SocketIO.evdata = {}
socketIO_client.SocketIO.emitting = False

SocketIO = socketIO_client.SocketIO
BaseNamespace = socketIO_client.BaseNamespace
