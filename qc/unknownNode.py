import maya.cmds as cmds


def inspect():
    return get_unknown_node()


def fix_selected(node):
    delete_unknown_node(node)


def fix_all(nodes):
    delete_all_unknown()


def get_unknown_node():
    """
    Get unknown node in the scene

    :return: list. names of the unknown nodes
    """
    return cmds.ls(type="unknown")


def delete_unknown_node(node):
    """
    Delete given unknown node

    :param node: str. name of the unknown node
    """
    locked_state = cmds.lockNode(node, q=1, l=1)
    if locked_state[0] == 1:
        cmds.lockNode(node, l=0)
    cmds.delete(node)


def delete_all_unknown():
    """
    Delete all unknown node in scene
    """
    cmds.delete(cmds.ls(type="unknown"))
