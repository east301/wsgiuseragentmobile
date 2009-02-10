# -*- coding: utf-8 -*-
import re
from uamobile.nonmobile import NonMobileUserAgent as NonMobile

from uamobile.factory.docomo import *
from uamobile.factory.ezweb import *
from uamobile.factory.softbank import *
from uamobile.factory.willcom import *

from IPy import IP

__all__ = ['detect', 'NonMobile']

DOCOMO_RE   = re.compile(r'^DoCoMo/\d\.\d[ /]')
SOFTBANK_RE = re.compile(r'^(?:(?:SoftBank|Vodafone|J-PHONE)/\d\.\d|MOT-)')
EZWEB_RE    = re.compile(r'^(?:KDDI-[A-Z]+\d+[A-Z]? )?UP\.Browser\/')
WILLCOM_RE  = re.compile(r'^Mozilla/3\.0\((?:DDIPOCKET|WILLCOM);|^Mozilla/4\.0 \(compatible; MSIE (?:6\.0|4\.01); Windows CE; SHARP/WS\d+SH; PPC; \d+x\d+\)')

def detect(environ, proxy_host=None):
    """
    parse HTTP user agent string and detect a mobile device.
    """
    try:
        useragent = environ['HTTP_USER_AGENT']
    except KeyError:
        return NonMobile(environ)

    if DOCOMO_RE.match(useragent):
        factory = DoCoMoUserAgentFactory()
    elif EZWEB_RE.match(useragent):
        factory = EZwebUserAgentFactory()
    elif SOFTBANK_RE.match(useragent):
        factory = SoftBankUserAgentFactory()
    elif WILLCOM_RE.match(useragent):
        factory = WillcomUserAgentFactory()
    else:
        return NonMobile(environ)

    device = factory.create(environ)

    # TODO
    hosts = []
    if proxy_host:
        if not isinstance(proxy_host, (list, tuple)):
            proxy_host = [proxy_host]

        for host in proxy_host:
            try:
                hosts.append(IP(host))
            except ValueError:
                raise ValueError('"%s" is not valid reverse proxy address' % host)

    device._proxy_host = hosts
    return device
