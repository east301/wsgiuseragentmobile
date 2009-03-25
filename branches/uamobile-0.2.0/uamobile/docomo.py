# -*- coding: utf-8 -*-
from uamobile.base import UserAgent, Display
from uamobile.docomodisplaymap import DISPLAYMAP_DOCOMO

class DoCoMoUserAgent(UserAgent):
    """
    NTT DoCoMo implementation
    see also http://www.nttdocomo.co.jp/service/imode/make/content/spec/useragent/index.html

    property "cache" returns cache size as kilobytes unit.

    property "status" means:
    TB | Browsers
    TC | Browsers with image off (only Available in HTTP 5.0)
    TD | Fetching JAR
    TJ | i-Appli
    """
    carrier = 'DoCoMo'
    short_carrier = 'D'

    def __init__(self, *args, **kwds):
        super(DoCoMoUserAgent, self).__init__(*args, **kwds)
        self.ser = None
        self.icc = None
        self.status = None
        self.s = None
        self.c = 5
        self.series = None
        self.vendor = None
        self.html_version = None

    def is_docomo(self):
        return True

    def get_cache_size(self):
        return self.c
    cache_size = property(get_cache_size)

    def get_bandwidth(self):
        return self.s
    bandwidth = property(get_bandwidth)

    def get_card_id(self):
        return self.icc
    card_id = property(get_card_id)

    def get_serialnumber(self):
        return self.ser
    serialnumber = property(get_serialnumber)

    def is_gps(self):
        return self.model in ('F661i', 'F505iGPS')

    def is_foma(self):
        return self.version == '2.0'

    def supports_cookie(self):
        return False

    def get_guid(self):
        """
        Get iMode ID(guid). For iMode ID, see
        http://www.nttdocomo.co.jp/service/imode/make/content/ip/index.html#imodeid
        """
        try:
            return self.environ['HTTP_X_DCMGUID']
        except KeyError:
            return None
    guid = property(get_guid)

    def make_display(self):
        """
        create a new Display object.
        """
        try:
            params = DISPLAYMAP_DOCOMO[self.model]
        except KeyError:
            params = {}

        if self.display_bytes:
            try:
                params['width_bytes'], params['height_bytes'] = self.display_bytes
            except ValueError:
                pass

        return Display(**params)
