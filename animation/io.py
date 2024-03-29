import maya.cmds as cmds


def create_export_node(attrs, node_name):
    """
    Create a dedicated temp node for exporting animation use,
    as sometimes it's necessary to have a fixed node name for mapping purpose

    :param attrs: list. list of attributes
    :param node_name: str. the name of the temp node
    :return: str. the node object
    """
    node = cmds.createNode('network', name=node_name)
    cmds.select(node)
    for attr in attrs:
        mobject = attr.split('.')[0]
        channel = attr.split('.')[-1]
        cmds.addAttr(longName=channel, at='float', keyable=1)
        cmds.connectAttr(
            '{}.{}'.format(mobject, channel),
            '{}.{}'.format(node_name, channel),
            force=1
            )
    return node


def export_attr_to_atom(fpath, start, end):
    """
    Export as .atom of the export node

    :param fpath: str. file path
    :param start: int. start frame
    :param end: int. end frame
    """
    cmds.file(
        fpath,
        type="atomExport",
        force=1,  # Overwrite
        exportSelected=1,
        options=(
            "precision=8;"
            "statics=1;"
            "baked=1;"
            "sdk=0;"
            "constraint=0;"
            "animLayers=0;"

            "selected=selectedOnly;"
            "whichRange=2;"
            "range={start}:{end};"
            "hierarchy=none;"
            "controlPoints=0;"
            "useChannelBox=1;"
            "options=keys;"

            "copyKeyCmd="
            "-animation objects"
            "-option keys"
            "-hierarchy none"
            "-controlPoints 0"
        ).format(start=start, end=end)
    )


def import_attr_from_atom(fpath, target):
    """
    Import .atom on the specified target mobject

    :param fpath: str. file path
    :param target: str. maya object
    """
    cmds.select(target)
    cmds.file(
        fpath,
        i=1,
        type="atomImport",
        options=(
            "targetTime=3;"
            "option=scaleReplace;"
            "match=string;"
            "selected=selectedOnly;"
            "search={import_node};"
            "replace={target_node};"
            "mapFile=;"
        ).format(import_node='', target_node=target)
    )
