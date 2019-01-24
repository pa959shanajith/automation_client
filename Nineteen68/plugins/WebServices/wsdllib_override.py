#-------------------------------------------------------------------------------
# Name:        wsdllib_override
# Purpose:     Override Zeep library's internal methods to deal with
#              application specific issues
#
# Author:      ranjan.agrawal
#
# Created:     03-10-2018
# Copyright:   (c) ranjan.agrawal 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import zeep
from cached_property import threaded_cached_property
from zeep.xsd.elements import Any
from zeep.client import ServiceProxy
from zeep.xsd.utils import NamePrefixGenerator, UniqueNameGenerator
from zeep.xsd.indicators import All, Choice, Group, Sequence

__all__ = ['zeep']

@property
def zeepClient_service_override(self):
    """The default ServiceProxy instance"""
    self._default_service = self.bind(
        service_name=self._default_service_name,
        port_name=self._default_port_name)
    if not self._default_service:
        raise ValueError("There is no default service defined. This is usually due to "
            "missing wsdl:service definitions in the WSDL")
    return self._default_service

def zeepClient_bind_override(self, service_name=None, port_name=None):
    """Create a new ServiceProxy for the given service_name and port_name.
    The default ServiceProxy instance (`self.service`) always referes to
    the first service/port in the wsdl Document.  Use this when a specific
    port is required.
    """
    if not self.wsdl.services:
        return

    if service_name:
        service = self.wsdl.services.get(service_name)
        if not service:
            raise ValueError("Service not found")
    else:
        service = next(iter(list(self.wsdl.services.values())), None)

    if port_name:
        port = service.ports.get(port_name)
        if not port:
            raise ValueError("Port not found")
    else:
        port = list(service.ports.values())[self.soaptype]
    return ServiceProxy(self, port.binding, **port.binding_options)

def create_message_header(self, operation, *args, **kwargs):
    envelope, http_headers = self._create(operation, args, kwargs)
    return http_headers

@threaded_cached_property
def zeep_xsd_indicators_elements_nested_override(self):
    """List of tuples containing the element name and the element"""
    result = []
    generator = NamePrefixGenerator()
    generator_2 = UniqueNameGenerator()

    for elm in self:
        if isinstance(elm, (All, Choice, Group, Sequence)):
            if elm.accepts_multiple:
                result.append((generator.get_name(), elm))
            else:
                for sub_name, sub_elm in elm.elements:
                    sub_name = generator_2.create_name(sub_name)
                result.append((None, elm))
        elif isinstance(elm, (Any, Choice)):
            result.append((generator.get_name(), elm))
        else:
            name = generator_2.create_name(elm.name)
            result.append((name, elm))
    zeep.xsd.indicators.inputParameterCount=len(result)
    return result


zeep.Client.service = zeepClient_service_override
zeep.Client.bind = zeepClient_bind_override
zeep.wsdl.soap.SoapBinding.create_message_header = create_message_header
zeep.xsd.indicators.inputParameterCount = 0
zeep.xsd.indicators.OrderIndicator.elements_nested = zeep_xsd_indicators_elements_nested_override
