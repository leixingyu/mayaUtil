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
    Class for nurbs curve transform node (which contains one or more shape)
    """

    VERSION = 0.1

    def __init__(self, shapes):
        """
        Initialization

        :param shapes: list. list of Shape object
        """
        self._shapes = shapes

    @classmethod
    def from_transform(cls, name):
        """
        Create the Curve object based on maya scene curve transform node

        :param name: str. transform of the curve node
        :return: Curve.
        """
        shape_names = hierarchy.get_shape_from_xform(name, check_unique_child=0)
        shapes = [shape.Shape.from_shape(s_name) for s_name in shape_names]

        return cls(shapes)

    @classmethod
    def from_dict(cls, data):
        """
        Create the Curve object based on dictionary data

        :param data: dict. dictionary containing one or more shape data
        :return: Curve.
        """
        shape_datas = data['shapes']
        shapes = list()
        for shape_data in shape_datas:
            s = shape.Shape.from_dict(shape_data)
            shapes.append(s)

        return cls(shapes)

    @property
    def shape_count(self):
        """
        :return: int. number of shape of the Curve object
        """
        return len(self._shapes)

    @property
    def shapes(self):
        """
        :return: list. Shape objects of the Curve object
        """
        return self._shapes

    def to_dict(self):
        """
        Export the current Curve object's info as dictionary

        :return: dict. Curve object's info
        """
        data = dict()
        data['version'] = self.VERSION
        data['shapes'] = list()
        for s in self._shapes:
            data['shapes'].append(s.to_dict())

        return data

    def rebuild_curve(self, name=None):
        """
        Re-build the curve in current scene using the Curve object

        :param name: str. name of the re-built curve
        """
        transforms = list()
        for s in self._shapes:
            s.rebuild_shape()
            transform_node = s.transform
            transforms.append(transform_node)

        if not name:
            name = 'random'
        util.merge_curves(name, transforms)
