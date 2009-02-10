# -*- coding: utf-8 -*-
from pkg_resources import resource_string
import simplejson
from IPy import IP

__all__ = ['IP', 'get_ip_addrs', 'get_ip']

def get_ip_addrs(carrier):
    carrier = carrier.lower()
    if carrier not in ('docomo', 'ezweb', 'softbank', 'willcom'):
        raise ValueError('invalid carrier name "%s"' % carrier)
    data = resource_string(__name__, 'data/cidr/%s.json' % carrier)
    return [tuple(x) for x in simplejson.loads(data)]

def get_ip(carrier, _memo={}):
    try:
        return _memo[carrier]
    except KeyError:
        _memo[carrier] = [IP('%s/%s' % x) for x in get_ip_addrs(carrier)]
        return _memo[carrier]

