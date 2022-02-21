import math


class Vector3(object):
    """
    Data type class for convenient Vector3 calculation

    Initialize:
    using list or tuple: v = Vector3([1, 2, 3])
    using list of arguments (3): v = Vector3(1, 2, 3)
    """

    def __init__(self, *args):
        self._vector = None

        # list
        if len(args) == 1:
            if isinstance(args[0], (tuple, list)):
                if len(args[0]) == 3:
                    self._vector = args[0]

        # three separate arguments
        elif len(args) == 3:
            self._vector = args

        if not self._vector:
            raise TypeError('initialize failure, check input type')

    def __repr__(self):
        return '{}({}, {}, {})'.format(
            self.__class__.__name__,
            self.x,
            self.y,
            self.z
        )

    def __neg__(self):
        return self.__class__(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        return self.__class__(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        try:
            return self.__class__(
                self.x / other,
                self.y / other,
                self.z / other
            )
        except ZeroDivisionError:
            raise ZeroDivisionError

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def __rsub__(self, other):
        return -self.__sub__(other)

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __radd__(self, other):
        return self.__add__(other)

    def normalize(self):
        if self._vector:
            return self / self.length

        return self.__class__.zero_vector()

    @classmethod
    def zero_vector(cls):
        return cls(0, 0, 0)

    @property
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    @property
    def x(self):
        return self._vector[0]

    @property
    def y(self):
        return self._vector[1]

    @property
    def z(self):
        return self._vector[2]

    def as_list(self):
        return [self.x, self.y, self.z]
