# -*- coding: utf-8 -*-
from pkg_resources import resource_string
import simplejson
from IPy import IP

from uamobile.cidrdata import crawler

__all__ = ['IP', 'get_ip_addrs', 'get_ip']

def get_ip_addrs(carrier):
    carrier = carrier.lower()
    if carrier not in ('docomo', 'ezweb', 'softbank', 'willcom', 'crawler'):
        raise ValueError('invalid carrier name "%s"' % carrier)

    if carrier == 'crawler':
        return crawler.DATA
    else:
        data = resource_string(__name__, 'data/cidr/%s.json' % carrier)
        res = []
        for ip, subnet in simplejson.loads(data):
            if subnet is not None:
                res.append('%s/%s' % (ip, subnet))
            else:
                res.append(ip)
        return res

def get_ip(carrier, _memo={}):
    try:
        return _memo[carrier]
    except KeyError:
        _memo[carrier] = [IP(x) for x in get_ip_addrs(carrier)]
        return _memo[carrier]

