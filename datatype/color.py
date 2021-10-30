class ColorRGB(object):

    def __init__(self, r, g, b):
        self._r = r
        self._g = g
        self._b = b

    @classmethod
    def red(cls):
        return cls(r=255, g=0, b=0)

    @classmethod
    def green(cls):
        return cls(r=0, g=255, b=0)

    @classmethod
    def blue(cls):
        return cls(r=0, g=0, b=255)

    @property
    def r(self):
        return self._r

    @property
    def g(self):
        return self._g

    @property
    def b(self):
        return self._b

    @property
    def r_normalized(self):
        return self._r/255.00

    @property
    def g_normalized(self):
        return self._g/255.00

    @property
    def b_normalized(self):
        return self._b/255.00
