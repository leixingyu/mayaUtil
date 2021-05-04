import maya.cmds as cmds

'''
def create_export_node(attrs, node_name):
    """ Create a temp node for export use

    :param attrs: [description]
    :type attrs: [type]
    :return: [description]
    :rtype: [type]
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
'''

def exportAttrToAtom(fpath, start, end):
    ''' Export as .atom of the export node'''

    cmds.file(
        fpath,
        type="atomExport",
        force=True,  # Overwrite
        exportSelected=True,
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
            "-controlPoints 0").format(start=start, end=end)
    )

def importAttrFromAtom(fpath, target):
    ''' Import .atom on the specified target mobject '''

    cmds.select(target)
    cmds.file(
        fpath,
        i=True,
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