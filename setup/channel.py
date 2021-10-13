import maya.cmds as cmds


def get_attrs_channel(node):
    """
    Get all attributes of the node displayed in the channel box
    TODO: test and clean up the code

    :param node: str. maya node name (cannot be a blendshape node)
    :return: list. attributes
    """

    attributes = list()

    attrs = cmds.listAttr(node)
    cb_attrs = cmds.listAnimatable(node)
    if attrs and cb_attrs:
        ordered_attrs = [
            attr for attr in attrs
            for cb_attr in cb_attrs
            if cb_attr.endswith(attr)
        ]
        attributes.extend(ordered_attrs)

    return attributes


def get_attrs_selected():
    """
    Get selected attribute of current node in the channelbox

    :return: list. full name of selected attributes
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
    """
    restore channel box to default setting

    :param obj: str. scene object
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
    """
    Reset selected attributes to default values
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


def get_attrs_unbinded(node):
    """
    Get full attribute list from a container un-bind section

    :param node: str. maya container node
    :return: list. attribute names
    """

    if cmds.container(node, isContainer=1, q=1):
        container = node
    else:
        return

    unbind_attrs = cmds.container(container, publishName=1, unbindAttr=1, q=1)
    return unbind_attrs


def connect_weighted(source, destination, ratio):
    """
    Weighted connection using expresssion

    :param source: str. source attribute
    :param destination: str. destination attribute
    :param ratio: float. weighting ratio between connection
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
    """
    Mapped connection using set driven key

    :param source: str. driver attribute
    :param src_min: float. driver minimum value
    :param src_max: float. driver maximum value
    :param destination: str. driven attribute
    :param dst_min: float. driven minimum value
    :param dst_max: float. driven maximum value
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
    """
    Break attribute connection: equivalent to channelbox break connection

    :param attr: str. attribute name
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
    """
    Validate if a attribute could be used in a connection

    :param attribute: str. attribute full name
    :return: list, [bool, string]. validation result and message
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
