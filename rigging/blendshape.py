import maya.cmds as cmds


def get_blendshape_targets(blendshape):
    """ Get all the target of a blendshape node

    :param blendshape: name of the blendshape node
    :type blendshape: string
    :return: all blendshape channels (aka. blendshape targets)
    :type: list
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
    """ Get blendshape nodes from output section of the channel box

    :param mobject: maya object
    :type mobject: string
    :return: blendshape nodes
    :rtype: list
    """

    cmds.select(mobject)
    output_attrs = cmds.channelBox('mainChannelBox', out=1, q=1)

    nodes = []
    for attr in output_attrs:
        node = attr.split('.')[0]
        if cmds.nodeType(node) == 'blendShape':
            nodes.append(node)

    return nodes


def get_input_blendshapes(mobject):
    """ Get blendshape nodes from input section of the channel box

    :param mobject: maya object
    :type mobject: string
    :return: blendshape nodes
    :rtype: list
    """

    nodes = []
    for node in cmds.listHistory(mobject):
        if cmds.nodeType(node) == 'blendShape':
            nodes.append(node)
    return nodes