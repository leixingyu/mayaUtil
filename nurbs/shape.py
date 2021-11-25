import maya.cmds as cmds

from ..common import hierarchy


class Shape(object):
    """
    The actual curve shape node
    """

    def __init__(self, pts, degree, form):
        self._transform = None
        self._pts = pts
        self._degree = degree
        self._form = form

    @classmethod
    def from_shape(cls, name):
        """
        Create shape object from shape name

        @param name: str. curve shape name
        """
        cvs = cmds.getAttr('{}.cv[*]'.format(name))
        degree = cmds.getAttr('{}.degree'.format(name))
        form = cmds.getAttr('{}.form'.format(name))

        return cls(cvs, degree, form)

    @classmethod
    def from_dict(cls, data):
        cvs = data['pts']
        degree = data['degree']
        form = data['form']

        return cls(cvs, degree, form)

    def to_dict(self):
        data = dict()

        data['pts'] = self._pts
        data['degree'] = self._degree
        data['form'] = self._form

        return data

    @property
    def transform(self):
        return self._transform

    @property
    def degree(self):
        return self._degree

    @property
    def form(self):
        return self._form

    @property
    def pt_count(self):
        return len(self._pts)

    @property
    def pts(self):
        return self._pts

    def rebuild_shape(self):
        """
        Rebuild the curve shape based on all the above info

        @return: str. shape node of the curve
        """
        c = cmds.curve(point=self._pts, degree=self._degree)

        if self._form == 1:
            cmds.closeCurve(c, ps=0)

        self._transform = c
        return hierarchy.get_shape_from_xform(c, check_unique_child=0)
