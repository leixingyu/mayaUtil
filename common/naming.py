import logging
import re

import maya.cmds as cmds


def check_duplicates(enable_rename=1):
    """
    Find all duplicated short names in scene and rename them

    :param enable_rename: bool, rename duplicated names
    """
    # Find all objects that have the same short name as another by find '|'
    duplicates = [f for f in cmds.ls() if '|' in f]
    # Sort them by hierarchy so no parent is renamed before a child.
    duplicates.sort(key=lambda obj: obj.count('|'), reverse=1)

    if not duplicates:
        logging.info("No Duplicates")
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
            logging.info("renamed %s to %s", name, new_name)
            check_duplicates(enable_rename=1)
        else:
            logging.info("Found Duplicates")


def is_name_unique(obj):
    """
    Check if the object short name is unique in the scene

    :param obj: str. scene object
    :return: bool. whether the object name is unique or not
    """
    short_name = obj.split('|')
    try:
        long_names = cmds.ls(short_name[-1], l=1)
    except:
        long_names = cmds.ls('*{}'.format(short_name[-1]), l=1)

    if len(long_names) > 1:
        return 0
    else:
        return 1


def remove_namespace(node):
    """
    Remove the top namespace of the node

    :param node: str. node name
    :return: str. new node name without top namespace
    """
    if ':' not in node:
        return node

    namespace, new_name = node.split(':', 1)
    if namespace not in cmds.namespaceInfo(listOnlyNamespaces=1):
        raise ValueError('namespace not found')
    cmds.namespace(removeNamespace=namespace, mergeNamespaceWithRoot=1)

    return new_name
