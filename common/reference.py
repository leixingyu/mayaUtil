import maya.cmds as cmds


def import_reference(node):
    """
    Import the corresponding reference file for a node into the current scene

    :param node: str. node name
    """
    if not cmds.referenceQuery(node, isNodeReferenced=1):
        return

    ref_node = cmds.referenceQuery(node, referenceNode=1)
    ref_file = cmds.referenceQuery(ref_node, filename=1)
    cmds.file(ref_file, importReference=1)


def load_reference(ref_node, is_load):
    """
    Load/Un-load reference in Maya based on the checkbox state

    :param ref_node: str. reference node name
    :param is_load: bool. whether to load or unload reference
    """
    if not is_load:
        cmds.file(unloadReference=ref_node)
    else:
        cmds.file(loadReference=ref_node)


def update_reference_path(ref_node, path):
    """
    Update the Maya reference path based on combo box active text

    :param ref_node: str. reference node name
    :param path: str. combo box active text
    """
    old_path = cmds.referenceQuery(ref_node, filename=1)
    cmds.file(path, loadReference=ref_node)
