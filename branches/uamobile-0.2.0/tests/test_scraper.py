# -*- coding: utf-8 -*-
from uamobile.utils import scraper

def test_cidr():
    def func(carrier):
        res = scraper.scrape_cidr(carrier)
        assert isinstance(res, list)
        for i, m in res:
            assert isinstance(i, str)
            assert isinstance(m, int)

    for s in ('docomo',
              'ezweb',
              'softbank',
              'willcom',
              ):
        yield func, s
