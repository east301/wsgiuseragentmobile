# -*- coding: utf-8 -*-
from uamobile import exceptions
from uamobile.base import UserAgent, Display
from uamobile.docomodisplaymap import DISPLAYMAP_DOCOMO

import re

VENDOR_RE = re.compile(r'([A-Z]+)\d')

FOMA_SERIES_4DIGITS_RE = re.compile(r'\d{4}')
FOMA_SERIES_3DIGITS_RE = re.compile(r'(\d{3}i|\d{2}[ABC])')

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

    HTML_VERSION_MAP = (((re.compile('[DFNP]501i'), '1.0'),
                         (re.compile('502i|821i|209i|651|691i|(?:F|N|P|KO)210i|^F671i$'), '2.0'),
                         (re.compile('(?:D210i|SO210i)|503i|211i|SH251i|692i|200[12]|2101V'), '3.0'),
                         (re.compile('504i|251i|^F671iS$|212i|2051|2102V|661i|2701|672i|SO213i|850i'), '4.0'),
                         (re.compile('eggy|P751v'), '3.2'),
                         (re.compile('505i|252i|900i|506i|880i|253i|P213i|901i|700i|851i$|701i|881i|^SA800i$|600i|^L601i$|^M702i(?:S|G)$|^L602i$'), '5.0'),
                         (re.compile('902i|702i|851iWM|882i|883i$|^N601i$|^D800iDS$|^P70[34]imyu$'), '6.0'),
                         (re.compile('883iES|903i|703i|904i|704i'), '7.0'),
                         (re.compile('905i|705i'), '7.1'),
                         (re.compile('906i|0[123]A'), '7.2'),
                         ))

    def __init__(self, *args, **kwds):
        super(DoCoMoUserAgent, self).__init__(*args, **kwds)
        self.ser = None
        self.icc = None
        self.status = None
        self.s = None
        self.c = 5

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

    def get_html_version(self):
        """
        returns supported HTML version like '3.0'.
        if unkwon, return None.
        """
        for pattern, value in self.HTML_VERSION_MAP:
            if pattern.search(self.model):
                return value
        return None
    html_version = property(get_html_version)

    def get_vendor(self):
        """
        returns vender code like 'SO' for Sony.
        if unkwon, returns None
        """
        matcher = VENDOR_RE.match(self.model)
        if matcher:
            return matcher.group(1)
        else:
            return None
    vendor = property(get_vendor)

    def get_series(self):
        """
        returns series name like '502i'.
        if unknow, return None.
        """
        if self.is_foma() and FOMA_SERIES_4DIGITS_RE.search(self.model):
            return 'FOMA'

        matcher = FOMA_SERIES_3DIGITS_RE.search(self.model)
        if matcher:
            return matcher.group(1)

        if self.model == 'P651ps':
            return '651'

        return None
    series = property(get_series)

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
