# -*- coding: utf-8 -*-
from pkg_resources import resource_string
import simplejson

def get_ip_addrs(carrier):
    carrier = carrier.lower()
    if carrier not in ('docomo', 'ezweb', 'softbank', 'willcom'):
        raise ValueError('invalid carrier name "%s"' % carrier)
    data = resource_string(__name__, 'data/cidr/%s.json' % carrier)
    return [tuple(x) for x in simplejson.loads(data)]

