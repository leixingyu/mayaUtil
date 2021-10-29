import maya.cmds as cmds


def get_dag_path(node=None):
    selection = om.MSelectionList()
    selection.add(node)
    dag_path = om.MDagPath()
    selection.getDagPath(0, dag_path)
    return dag_path


def check_duplicates(enable_rename=True):
    """
    Find all duplicated short names in scene and rename them

    :param enable_rename: bool, allow renaming for duplicated names
    """

    import re
    # Find all objects that have the same short name as another by find '|'
    duplicates = [f for f in cmds.ls() if '|' in f]
    # Sort them by hierarchy so no parent is renamed before a child.
    duplicates.sort(key=lambda obj: obj.count('|'), reverse=True)

    if not duplicates:
        print("No Duplicates")
    else:
        if enable_rename:
            name = duplicates[0]
            match_short = re.compile("[^|]*$").search(name)
            short_name = match_short.group(0)

            # extract the numeric suffix
            match_suffix = re.compile(".*[^0-9]").match(short_name)
            if match_suffix:
                suffix = match_suffix.group(0)
            else:
                suffix = short_name

            # add '#' as the suffix, maya will find the next available number
            new_name = cmds.rename(name, '{}#'.format(suffix))
            print("renamed {} to {}".format(name, new_name))
            check_duplicates(enable_rename=True)
        else:
            print("Found Duplicates")


def is_name_unique(obj):
    """
    Check if the object short name is unique in the scene

    :param obj: str. scene object
    :return: bool. whether the object name is unique or not
    """
    short_name = obj.split('|')
    try:
        long_names = cmds.ls(short_name[-1], l=True)
    except:
        long_names = cmds.ls('*{}'.format(short_name[-1]), l=True)

    if len(long_names) > 1:
        return 0
    else:
        return 1


def mirror_locator():
    """
    Mirrors locators from Left side to Right side
    TODO: rework this
    """

    selection = cmds.ls(selection=True)
    if not selection:
        raise RuntimeError("no locator selected")
    else:
        cmds.select(selection, hi=True)
        left_locs = cmds.ls(selection=True, transforms=True)
        right_locs = [loc.replace('_L_', '_R_') for loc in left_locs]

        if len(left_locs) == len(right_locs):
            for i in range(len(left_locs)):
                translation = cmds.getAttr('{}.t'.format(left_locs[i]))
                cmds.setAttr('{}.tx'.format(right_locs[i]), -translation[0][0])
                cmds.setAttr('{}.ty'.format(right_locs[i]), translation[0][1])
                cmds.setAttr('{}.tz'.format(right_locs[i]), translation[0][2])
                rotation = cmds.getAttr('{}.r'.format(left_locs[i]))
                cmds.setAttr('{}.rx'.format(right_locs[i]), rotation[0][0])
                cmds.setAttr('{}.ry'.format(right_locs[i]), -rotation[0][1])
                cmds.setAttr('{}.rz'.format(right_locs[i]), -rotation[0][2])
        else:
            raise RuntimeError("left and right locators not match")

