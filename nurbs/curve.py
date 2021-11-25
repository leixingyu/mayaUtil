"""
API:
crv = c.Curve.from_transform('nurbsCircle1')
d = crv.to_dict()

# you can export this dictionary as json and import it back

crv = c.Curve.from_dict(d)
crv.rebuild_curve('test')
"""

from . import util
from . import shape
from ..common import hierarchy


class Curve(object):
    """
    The nurbs curve transform node, may contain more than one shape
    """

    VERSION = 0.1

    def __init__(self, shapes):
        self._shapes = shapes

    @classmethod
    def from_transform(cls, name):
        shape_names = hierarchy.get_shape_from_xform(name, check_unique_child=0)
        shapes = [shape.Shape.from_shape(s_name) for s_name in shape_names]

        return cls(shapes)

    @classmethod
    def from_dict(cls, data):
        shape_datas = data['shapes']

        shapes = list()
        for shape_data in shape_datas:
            shape = shape.Shape.from_dict(shape_data)
            shapes.append(shape)

        return cls(shapes)

    def to_dict(self):
        data = dict()

        data['version'] = self.VERSION
        data['shapes'] = list()
        for shape in self._shapes:
            data['shapes'].append(shape.to_dict())

        return data

    def rebuild_curve(self, name=None):
        transforms = list()
        for shape in self._shapes:
            shape.rebuild_shape()
            transform_node = shape.transform
            transforms.append(transform_node)

        if not name:
            name = 'random'
        util.merge_curves(name, transforms)

    @property
    def shape_count(self):
        return len(self._shapes)

    @property
    def shapes(self):
        return self._shapes
