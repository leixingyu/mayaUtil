import maya.cmds as cmds

from ..common import hierarchy


class Shape(object):
    """
    Class for representing the actual curve shape node
    """

    def __init__(self, pts, degree, form):
        """
        Initialization

        :param pts: list. point tuples containing x,y,z coordinates
        :param degree: int. curve degree
        :param form: int. curve form enum
        """
        self._transform = None
        self._pts = pts
        self._degree = degree
        self._form = form

    @classmethod
    def from_shape(cls, name):
        """
        Create shape object from a maya scene curve shape

        :param name: str. curve shape name
        :return: Shape
        """
        cvs = cmds.getAttr('{}.cv[*]'.format(name))
        degree = cmds.getAttr('{}.degree'.format(name))
        form = cmds.getAttr('{}.form'.format(name))

        return cls(cvs, degree, form)

    @classmethod
    def from_dict(cls, data):
        """
        Create shape object from a dictionary

        :param data: dict. shape data
        :return: Shape
        """
        cvs = data['pts']
        degree = data['degree']
        form = data['form']

        return cls(cvs, degree, form)

    @property
    def transform(self):
        """
        :return: str. transform node of the shape
        """
        return self._transform

    @property
    def degree(self):
        """
        :return: int. degree of the shape
        """
        return self._degree

    @property
    def form(self):
        """
        :return: int. shape form enum
        """
        return self._form

    @property
    def pt_count(self):
        """
        :return: int. number of cv points in the shape
        """
        return len(self._pts)

    @property
    def pts(self):
        """
        :return: list. point tuples containing x,y,z coordinates of each point
        """
        return self._pts

    def to_dict(self):
        """
        Export the current shape object as a dictionary

        :return: dict. shape data in a dictionary
        """
        data = dict()

        data['pts'] = self._pts
        data['degree'] = self._degree
        data['form'] = self._form

        return data

    def rebuild_shape(self):
        """
        Rebuild the curve shape based on all the above info

        :return: str. shape node of the curve
        """
        c = cmds.curve(point=self._pts, degree=self._degree)

        if self._form == 1:
            cmds.closeCurve(c, ps=0)

        self._transform = c
        return hierarchy.get_shape_from_xform(c, check_unique_child=0)
