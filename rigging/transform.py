import maya.cmds as cmds

from ..setup import outliner


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
    :param transform: str. transform node
    """
    outliner.match_xform(offset, transform)

    cmds.parent(ctrl, offset, relative=1)
    cmds.makeIdentity(ctrl, apply=1, t=1, r=1, s=1)