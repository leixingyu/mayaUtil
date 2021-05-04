import maya.cmds as cmds


def get_attrs_selected():
    """ Get selected attribute of current node in the channelbox

    :return: full name of selected attributes
    :rtype: list
    """

    selections = cmds.ls(selection=1)
    channels = cmds.channelBox(
        'mainChannelBox',
        selectedMainAttributes=1,
        q=1
    )

    if not len(selections) == 1:
        return

    attrs = ['{}.{}'.format(selections[0], channel) for channel in channels]
    return attrs


def restore_channel(obj):
    """ restore channel box to default setting

    :param obj: scene object
    """

    kwargs = {
        'lock': 0,
        'keyable': 1,
    }

    for transform in ['t', 'r', 's']:
        for axis in ['x', 'y', 'z']:
            cmds.setAttr('{}.{}{}'.format(obj, transform, axis), **kwargs)
    cmds.setAttr('{}.visibility'.format(obj), **kwargs)
    cmds.setAttr('{}.visibility'.format(obj), 1)


def reset_attrs():
    """ Reset selected attributes to default values
    """

    selected_channels = cmds.channelBox(
        'mainChannelBox',
        selectedMainAttributes=1,
        selectedOutputAttributes=1,
        selectedShapeAttributes=1,
        q=1
        )

    for selection in cmds.ls(selection=1):
        if not selected_channels:
            selected_channels = cmds.listAttr(
                selection,
                keyable=1,
                read=1,
                write=1,
                connectable=1
                ) or []

        for channel in selected_channels:
            attribute = "{0}.{1}".format(selection, channel)
            if not cmds.getAttr(attribute, lock=1):
                defaultValue = cmds.attributeQuery(channel, node=selection, listDefault=1)
                if defaultValue:
                    cmds.setAttr(attribute, defaultValue[0])


def get_unbinded_attrs(node):
    """ Get full attribute list from a container un-bind section

    :param node: maya container node
    :type node: string
    :return: attribute names
    :rtype: list
    """

    if cmds.container(node, isContainer=1, q=1):
        container = node
    else:
        return

    unbind_attrs = cmds.container(container, publishName=1, unbindAttr=1, q=1)
    return unbind_attrs


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


def connect_weighted(source, destination, ratio):
    """ Weighted connection using expresssion

    :param source: source attribute
    :type source: string
    :param destination: destination attribute
    :type destination: string
    :param ratio: weighting ratio between connection
    :type ratio: float
    """

    try:
        cmds.expression(
            string='{}={}*{}'.format(destination, source, ratio),
            alwaysEvaluate=1,
            unitConversion='all'
        )
    except Exception as e:
        raise e


def connect_drivenkey(source, src_min, src_max, destination, dst_min, dst_max):
    """ Mapped connection using set driven key

    :param source: driver attribute
    :type source: string
    :param src_min: driver minium value
    :type src_min: float
    :param src_max: driver maxium value
    :type src_max: float
    :param destination: driven attribute
    :type destination: string
    :param dst_min: driven minium value
    :type dst_min: float
    :param dst_max: driven maxium value
    :type dst_max: float
    """

    driven = destination.split('.')[0]
    attribute = destination.split('.')[-1]

    try:
        cmds.setDrivenKeyframe(
            driven,
            attribute=attribute,
            value=dst_min,
            currentDriver=source,
            driverValue=src_min
        )

        cmds.setDrivenKeyframe(
            driven,
            attribute=attribute,
            value=dst_max,
            currentDriver=source,
            driverValue=src_max
        )
    except Exception as e:
        raise e


# source: https://discourse.techart.online/t/cbdeleteconnection-in-python/1179
def delete_connection(attr):
    """ Break attribute connection: equivalent to channelbox break connection

    :param attr: attribute name
    :type attr: string
    """

    if cmds.connectionInfo(attr, isDestination=1):
        attr = cmds.connectionInfo(attr, getExactDestination=1)
        is_readonly = cmds.ls(attr, ro=1)
        # delete -icn doesn't work if destination attr is readOnly
        if is_readonly:
            source = cmds.connectionInfo(attr, sourceFromDestination=1)
            cmds.disconnectAttr(source, attr)
        else:
            cmds.delete(attr, icn=1)


def validate_connection(attribute):
    """ Validate if a attibute could be used in a connection

    :param attribute: attribute full name
    :type attribute: string
    :return: validation result and message
    :rtype: list, [bool, string]
    """

    obj, channel = attribute.split('.')

    if '.' not in attribute:
        return False, '*{}* is not an attribute'.format(attribute)

    if not cmds.ls(obj):
        return False, '*{}* object does not exist'.format(obj)

    if not cmds.attributeQuery(channel, node=obj, ex=1):
        return False, '*{}* attribute does not exist'.format(attribute)

    if not (cmds.attributeQuery(channel, node=obj, keyable=1)
            and not cmds.getAttr(attribute, lock=1)):
        return False, '*{}* attribute not keyable or locked'.format(attribute)

    if cmds.connectionInfo(attribute, isDestination=1):
        return False, '*{}* attribute already connected'.format(attribute)

    return True, 'Validation Complete'
