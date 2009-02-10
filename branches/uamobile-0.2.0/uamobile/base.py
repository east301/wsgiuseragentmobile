# -*- coding: utf-8 -*-
from uamobile import cidr

class UserAgent(object):
    """
    Base class representing HTTTP user agent.
    """

    def __init__(self, environ):
        try:
            self.useragent = environ['HTTP_USER_AGENT']
        except KeyError, e:
            self.useragent = ''
        self.environ = environ
        self.model = ''
        self.version = ''
        self._display = None

    def __repr__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.useragent)

    def __str__(self):
        return self.useragent

    def get_display(self):
        """
        returns Display object.
        """
        if self._display is None:
            self._display = self.make_display()
        return self._display
    display = property(get_display)

    def make_display(self):
        raise NotImplementedError

    def is_docomo(self):
        """
        returns True if the agent is DoCoMo.
        """
        return False

    def is_ezweb(self):
        """
        returns True if the agent is EZweb.
        """
        return False

    def is_tuka(self):
        """
        returns True if the agent is TU-Ka.
        """
        return False

    def is_softbank(self):
        """
        returns True if the agent is Softbank.
        """
        return False

    def is_vodafone(self):
        """
        returns True if the agent is Vodafone (now SotBank).
        """
        return False

    def is_jphone(self):
        """
        returns True if the agent is J-PHONE (now softbank).
        """
        return False

    def is_willcom(self):
        """
        returns True if the agent is Willcom.
        """
        return False

    def is_airhphone(self):
        """
        returns True if the agent is AirH'PHONE.
        """
        return False

    def is_wap1(self):
        return False

    def is_wap2(self):
        return False

    def is_nonmobile(self):
        return False

    def supports_cookie(self):
        """
        returns True if the agent supports HTTP cookie.
        """
        raise NotImplementedError

    def is_bogus(self):
        """
        return True if the client isn't accessing via gateways of
        japanese mobile carrier
        """
        try:
            remote_addr = self.environ['REMOTE_ADDR']
        except KeyError:
            return True

        forwared_for = self.environ.get('HTTP_X_FORWARDED_FOR')
        if forwared_for and self._proxy_host:
            forwared_for = forwared_for.split(',', 1)[0].strip()

            # check REMOTE_ADDR is included in trusted reverse
            # proxy address
            for addr in self._proxy_host:
                if remote_addr in addr:
                    # override remote addr
                    remote_addr = forwared_for
                    break

        try:
            remote_addr = cidr.IP(remote_addr)
        except ValueError:
            return True

        for addr in cidr.get_ip(self.carrier):
            if remote_addr in addr:
                return False

        return True


class Display(object):
    """
    Display information for mobile devices.
    """

    def __init__(self, width=None, height=None, depth=None, color=None,
                 width_bytes=None, height_bytes=None):
        self.width = width or 0
        self.height = height or 0
        self.depth = depth or 0
        self.color = color or 0
        self.width_bytes = width_bytes
        self.height_bytes = height_bytes

    def is_qvga(self):
        return self.width >= 240

    def is_vga(self):
        return self.width >= 480
