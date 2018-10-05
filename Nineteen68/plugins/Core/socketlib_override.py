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

import logging
import socketIO_client
from socketIO_client import TimeoutError, ConnectionError

__all__ = ['SocketIO','BaseNamespace']

""" Override SocketIO library's warn method used for logging.
    This is needed because this library doesn't gives anything to stdout or stderr
    on exception/warning. Hence Adding custom check and raising exception. Ref #1847.
"""
def socketIO_warn_override(self, msg, *attrs):
    self._log(logging.WARNING, msg, *attrs)
    if ("[SSL: CERTIFICATE_VERIFY_FAILED]" in msg) or ("hostname" in msg and "doesn't match " in msg):
        raise ValueError("[Certifiate Mismatch] "+ msg)

""" Override SocketIO library's _transport method used for generating new Transport instance.
    This is needed because this library opens new instance after invoking disconnect. Ref #1823.
"""
@property
def socketIO_transport_override(self):
    if self._opened or self._wants_to_close:
        return self._transport_instance
    self._engineIO_session = self._get_engineIO_session()
    self._negotiate_transport()
    self._connect_namespaces()
    self._opened = True
    self._reset_heartbeat()
    return self._transport_instance

""" Override SocketIO library's _close method used for closing a Transport instance.
    This is needed because this library never actually closes the connection.
    Ref: https://github.com/invisibleroads/socketIO-client/issues/176
    Ref: https://github.com/invisibleroads/socketIO-client/pull/126
"""
def socketIO_close_override(self):
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

""" Add close method in XHR_PollingTransport for closing a Transport instance connection.
    This is needed because this library never actually closes the connection.
    Ref: https://github.com/invisibleroads/socketIO-client/issues/176
    Ref: https://github.com/invisibleroads/socketIO-client/pull/126
"""
def socketIO_XHR_close_override(self):
    pass

""" Add close method in WebsocketTransport for closing a Transport instance connection.
    This is needed because this library never actually closes the connection.
    Ref: https://github.com/invisibleroads/socketIO-client/issues/176
    Ref: https://github.com/invisibleroads/socketIO-client/pull/126
"""
def socketIO_WS_close_override(self):
    self._connection.close()

socketIO_client.SocketIO._warn = socketIO_warn_override
socketIO_client.SocketIO._close = socketIO_close_override
socketIO_client.SocketIO._transport = socketIO_transport_override
socketIO_client.XHR_PollingTransport.close = socketIO_XHR_close_override
socketIO_client.WebsocketTransport.close = socketIO_WS_close_override


SocketIO = socketIO_client.SocketIO
BaseNamespace = socketIO_client.BaseNamespace
