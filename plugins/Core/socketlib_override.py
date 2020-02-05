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
#from io import StringIO
from uuid import uuid4 as uuid
from threading import Timer
import socketIO_client
import storage
from socketIO_client.exceptions import *
from socketIO_client.transports import *

CHUNK_MAX_LIMIT = 15*1024*1024 # 15 MB
CHUNK_SIZE = 10*1024*1024 # 10 MB
PACKET_TIMEOUT = 60 # Seconds
VERIFY_HOSTNAME = False
PAGINATE_INDEX = "p@gIn8"

try:
    store = storage.SQLite()
    #store = storage.InMemory()
except:
    store = storage.InMemory()


__all__ = ['SocketIO','BaseNamespace']


##import requests
##def http_adapter_init_poolmanager(self, connections, maxsize, block=requests.adapters.DEFAULT_POOLBLOCK, **pool_kwargs):
##    self._pool_connections = connections
##    self._pool_maxsize = maxsize
##    self._pool_block = block
##    self.poolmanager = requests.adapters.PoolManager(num_pools=connections, maxsize=maxsize,
##        block=block, strict=True, assert_hostname=VERIFY_HOSTNAME, **pool_kwargs)
##requests.adapters.HTTPAdapter.init_poolmanager = http_adapter_init_poolmanager

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
        kw['sslopt'] = {'cert_reqs': ssl.CERT_REQUIRED, 'ca_certs': http_session.verify, 'check_hostname': VERIFY_HOSTNAME}  ## New Change
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

""" Override SocketIO library's transports.get_response method used for processing
    XHR-polling response. This is needed because this library doesn't handle NGINX 504 Error.
"""
def socketIO_get_response(request, *args, **kw):
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
        if status_code == 504 and "Nineteen68 Error" in response.text: raise ValueError("Nineteen68 Server Unavailable")
        raise ConnectionError('unexpected status code (%s %s)' % (
            status_code, response.text))
    return response

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
    This is needed to free up memory consumed by stored packet, send next packet in queue.
"""
def socketIO_on_data_ack(self, pack_id, *args):
    if (self._io.activeTimer != None and self._io.activeTimer.isAlive()):
        self._io.activeTimer.cancel()
    idx = pack_id.split('_')
    idx = idx[1] if len(idx) == 2 else None
    #print("Ack'd "+str(pack_id))
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
    fargs = (packid,) + fargs
    idx = packid.split('_')
    send_now = not store.has_packet
    store.save_packet(int(idx[0]), (idx[1] if len(idx) == 2 else None), [event, fargs, fkw])
    if send_now: self.send_pckt(event, *fargs, **fkw)

""" Override SocketIO library's emit method used for sending data.
    This is needed because this library doesn't support packet size larger than 100 MB
"""
def socketIO_emit(self, event, *args, **kw):
    pack_id = store.get_id
    if len(args) == 0 or (len(args) > 0 and type(args[0]) == bool):
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
    #print("Sending "+str(args[0]))
    try:
        self._emit(event, *args, **kw)
    except:
        pass
    self.activeTimer = Timer(PACKET_TIMEOUT, self.send_pckt, (event,) + args, kw)
    self.activeTimer.start()
    del args


socketIO_client.parsers._read_packet_length = socketIO_read_packet_length
socketIO_client.parsers._read_packet_text = socketIO_read_packet_text
socketIO_client.transports.get_response = socketIO_get_response
socketIO_client.XHR_PollingTransport.close = socketIO_XHR_close
socketIO_client.WebsocketTransport.__init__ = socketIO_WS_init
socketIO_client.WebsocketTransport.close = socketIO_WS_close
socketIO_client.BaseNamespace.on_data_ack = socketIO_on_data_ack
socketIO_client.SocketIO.save_pckt = socketIO_save_pckt
socketIO_client.SocketIO.send_pckt = socketIO_send_pckt
socketIO_client.SocketIO._emit = socketIO_client.SocketIO.emit
socketIO_client.SocketIO.emit = socketIO_emit
socketIO_client.SocketIO._warn = socketIO_warn
socketIO_client.SocketIO._close = socketIO_close
socketIO_client.SocketIO._transport = socketIO_transport
socketIO_client.SocketIO.waiting_for_close = socketIO_waiting_for_close
socketIO_client.SocketIO.wait = socketIO_wait
socketIO_client.SocketIO.activeTimer = None

SocketIO = socketIO_client.SocketIO
BaseNamespace = socketIO_client.BaseNamespace