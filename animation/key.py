import maya.cmds as cmds


def bake_keys(nodes, start, end):
    """
    Bake animation of specified nodes

    :param nodes: [str]. node names to bake
    :param start: int. start frame
    :param end: int. end frame
    """
    # turn off evaluation so the viewport won't update
    eval_mode = cmds.evaluationManager(query=1, mode=1)[0]
    if eval_mode != 'off':
        cmds.evaluationManager(mode='off')
    cmds.refresh(suspend=1)

    try:
        cmds.bakeResults(
            nodes,
            time=(start, end),
            simulation=1,
            disableImplicitControl=1,
            preserveOutsideKeys=1,
            removeBakedAnimFromLayer=0,
            bakeOnOverrideLayer=0,
            minimizeRotation=1
        )
    except Exception:
        raise Exception
    finally:
        cmds.refresh(suspend=0)
        cmds.evaluationManager(mode=eval_mode)


def copy_keys(source, destination, start, end):
    """
    Copy keyframes from one channel to another within a given range.
    if keyframes are not present, the start and end frames are set so values
    are fixed

    :param source: str. source attribute full name (e.g. 'cube1.tx')
    :param destination: str. destination/target attribute full name
                        (e.g. 'sphere1.tx')
    :param start: int. start frame
    :param end: int. end frame
    """
    src_node, src_attr = source.split('.')
    dst_node, dst_attr = destination.split('.')

    # copy keyframes between the range
    keys = cmds.copyKey(
        src_node,
        time=(start, end),
        attribute=src_attr,
        option="keys"
    )
    if keys:
        cmds.pasteKey(dst_node, attribute=dst_attr, option="insert")

    # set keyframes at start and end just in case
    cmds.currentTime(start)
    cmds.setKeyframe(
        dst_node,
        attribute=dst_attr,
        time=start,
        value=cmds.getAttr(source)
    )

    cmds.currentTime(end)
    cmds.setKeyframe(
        dst_node,
        attribute=dst_attr,
        time=end,
        value=cmds.getAttr(source)
    )
