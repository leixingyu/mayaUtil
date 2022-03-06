import maya.cmds as cmds
from pipelineUtil.common import algorithm


def get_blendshape_targets(blendshape):
    """
    Get all the target of a blendshape node

    :param blendshape: str. name of the blendshape node
    :return: list. all blendshape channels (aka. blendshape targets)
    """
    # method 1
    all_attrs = cmds.aliasAttr(blendshape, q=1)
    # This returns you a list in the form "targetName", "weight[x]"
    # then process the list to get the target names of weights
    targets = [attr for attr in all_attrs if 'weight' not in attr]

    # method 2
    # listAttr doesn't work like other non-blendshape node
    targets = cmds.listAttr(blendshape+'.weight', multi=1)

    return targets


def get_output_blendshapes(mobject):
    """
    Get blendshape nodes from destination (output) of node

    :param mobject: str. maya object
    :return: list. blendshape nodes
    """
    blendshapes = cmds.listConnections(mobject, d=1, type='blendShape')
    return algorithm.get_list_unique(blendshapes)


def get_container_blendshapes(mobject):
    """
    Get blendshape nodes from container in source (input)

    :param mobject: str. maya container node
    :return: list. blendshape nodes
    """
    nodes = list()
    for node in cmds.listHistory(mobject):
        if cmds.nodeType(node) == 'blendShape':
            nodes.append(node)
    return nodes
