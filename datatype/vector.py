import math


class Vector(object):
    """
    Data type class for convenient vector3 calculation in maya

    initialize:
    using list or tuple: v = Vector([1, 2, 3])
    using list of arguments (3): v = Vector(1, 2, 3)
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
        return Vector(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        return Vector(other * self.x, other * self.y, other * self.z)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __rsub__(self, other):
        return -self.__sub__(other)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __radd__(self, other):
        return self.__add__(other)

    def normalize(self):
        if self._vector:
            try:
                return Vector(
                    self.x / self.length,
                    self.y / self.length,
                    self.z / self.length
                )
            except ZeroDivisionError:
                pass

        return Vector(0, 0, 0)

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

    @property
    def as_list(self):
        return [self.x, self.y, self.z]
