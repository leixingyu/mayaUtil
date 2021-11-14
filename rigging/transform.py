import maya.cmds as cmds
from maya import OpenMaya as om

from ..common import hierarchy


def colorize_rgb_normalized(node, r, g, b):
    """
    Colorize transform

    :param node: str. transform node
    :param r: float. normalized red channel value
    :param g: float. normalized green channel value
    :param b: float. normalized blue channel value
    """
    if cmds.nodeType(node) != 'transform':
        return

    cmds.setAttr('{}.overrideEnabled'.format(node), 1)
    cmds.setAttr('{}.overrideRGBColors'.format(node), 1)
    cmds.setAttr('{}.overrideColorRGB'.format(node), r, g, b)


def clear_transform(ctrl, offset, transform):
    """
    Use offset group to clear out control's position and rotation
    Used to match controller to the transform of a joint, while keeping 0 value

    :param ctrl: str. controller transform
    :param offset: str. offset group name
    :param transform: str. transform node, typically a joint
    """
    match_xform(offset, transform)

    cmds.parent(ctrl, offset, relative=1)
    cmds.makeIdentity(ctrl, apply=1, t=1, r=1, s=1)


def match_xform(source, target):
    """
    Match source rotation and translation to the target

    :param source:
    :param target:
    :return:
    """

    pos = cmds.xform(target, q=1, t=1, ws=1)
    rot = cmds.xform(target, q=1, ro=1, ws=1)

    cmds.move(pos[0], pos[1], pos[2], source)
    cmds.rotate(rot[0], rot[1], rot[2], source)


def get_dag_path(node=None):
    """
    Get DAG path of the specified node

    :param node: str. maya object
    :return: str. DAG path
    """
    selection = om.MSelectionList()
    selection.add(node)
    dag_path = om.MDagPath()
    selection.getDagPath(0, dag_path)
    return dag_path
