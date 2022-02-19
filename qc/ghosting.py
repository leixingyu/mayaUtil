import maya.cmds as cmds
import maya.mel as mel


def inspect():
    return get_ghosting_node()


def fix_selected(node):
    unghost_node(node)


def fix_all(nodes):
    unghost_all()


def get_ghosting_node():
    """
    Get ghosting node in the scene

    :return: list. list of ghosting node names
    """
    return cmds.ls(ghost=1)


def unghost_node(node):
    """
    Set ghosting to false on a node

    :param node: str. node name to un-ghost
    """
    cmds.setAttr('{}.ghosting'.format(node), 0)
    cmds.setAttr('{}.ghostingControl'.format(node), 0)


def unghost_all():
    """
    Set ghosting to false for all nodes
    """
    mel.eval("unGhostAll;")

