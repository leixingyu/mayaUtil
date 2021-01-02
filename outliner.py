#!/usr/bin/env python
""" Provide supporting functions for arranging objects in outliner

"""

import maya.cmds as cmds

__author__ = "Xingyu Lei"
__maintainer__ = "Xingyu Lei"
__email__ = "wzaxzt@gmail.com"
__status__ = "development"


def get_root_node(obj, type_specified=None):
    """Get the root of the object in the hierarchy

    :param obj: scene object
    :param type_specified: (optional), str, restrict the root node type
    :return: root, scene object
    """

    root = None

    # check current node
    if not type_specified:
        root = obj
    else:
        if cmds.objectType(obj, isType=type_specified):
            root = obj

    # search until reached to scene root
    if not type_specified:
        while cmds.listRelatives(obj, parent=1):
            obj = cmds.listRelatives(obj, parent=1)[0]
    else:
        while cmds.listRelatives(obj, parent=1):
            parent = cmds.listRelatives(obj, parent=1)[0]
            if cmds.objectType(parent, isType=type_specified):
                root = parent
            obj = parent

    return root


def get_hierarchy_of_type(root, type_specified):
    """ get all children (including root) in hierarchy of a certain type

    :param root: single scene object
    :param type_specified: str
    :return: list
    """

    obj_list = []
    children = cmds.listRelatives(root, children=1)
    if not children:
        # the root is already at the top
        if cmds.objectType(root, isType=type_specified):
            obj_list.append(root)
    else:
        # the current object has children
        for child in children:
            obj_list += get_hierarchy_of_type(child, type_specified)

    return obj_list


def delete_hierarchy_except_type(roots, type_specified):
    """ delete all other types of objects under hierarchy of root
    note: the function cannot re-parent shape node to another transform
    but since it is always on top, it is safe to delete before hand

    :param roots: scene obj, list or single
    :param type_specified: str
    """

    if not isinstance(roots, list):
        roots = [roots]

    for root_obj in roots:
        children = cmds.listRelatives(root_obj, children=1)
        if not children:
            # the current object is the top object
            if not cmds.objectType(root_obj, isType=type_specified):
                cmds.delete(root_obj)
        else:
            # the current object has children
            for child in children:
                # the child is not top object or different type, re-parent
                if not cmds.objectType(root_obj, isType=type_specified):
                    cmds.parent(child,
                                cmds.listRelatives(root_obj, parent=1))
                delete_hierarchy_except_type(child, type_specified)

            # children moved under another parent, delete original parent
            if not cmds.objectType(root_obj, isType=type_specified):
                cmds.delete(root_obj)


def delete_hierarchy_except_node(roots, type_specified):
    """ delete all other types of objects under hierarchy of root
    note: the function cannot re-parent shape node to another transform
    but since it is always on top, it is safe to delete before hand

    :param roots: scene obj, list or single
    :param type_specified: str
    """

    if not isinstance(roots, list):
        roots = [roots]

    for root_obj in roots:
        children = cmds.listRelatives(root_obj, children=1)
        if not children:
            # the current object is the top object
            if not cmds.listConnections(root_obj, type=type_specified):
                cmds.delete(root_obj)
        else:
            # the current object has children
            for child in children:
                # the child is not top object or different type, re-parent
                if not cmds.listConnections(root_obj, type=type_specified):
                    cmds.parent(child,
                                cmds.listRelatives(root_obj, parent=1))
                delete_hierarchy_except_node(child, type_specified)

            # children moved under another parent, delete original parent
            if not cmds.listConnections(root_obj, type=type_specified):
                cmds.delete(root_obj)


def delete_hierarchy_shape(roots):
    """ Delete all shapes under the given root

    :param roots: scene object, list or single
    """

    if not isinstance(roots, list):
        roots = [roots]

    for root in roots:
        nodes = cmds.listRelatives(root, ad=1)
        shapes = cmds.ls(nodes, shapes=1)
        if shapes:
            cmds.delete(shapes)


def get_shape_from_transform(transform, enable_result_only=True,
                             check_unique_child=True):
    """ get shape nodes under the transform

    :param transform: single scene object
    :param enable_result_only: bool, get only the result shape
    :param check_unique_child: bool, check if transform has multiple shapes
    :return: list, the shape node
    """

    shapes = cmds.listRelatives(transform, shapes=1)
    shapes_result = [shape for shape in shapes if 'Orig' not in shape]

    if check_unique_child:
        assert len(shapes_result) != 0, "no shape node found"
        assert len(shapes_result) == 1, "multiple shape node found in {} " \
                                        "they are: {}"\
            .format(transform, str(shapes_result))

    if enable_result_only:
        return shapes_result
    else:
        return shapes


def batch_parent(obj_list, parent):
    """ Grouping multiple objects to the same parent

    :param obj_list: list
    :param parent: scene object
    """
    for item in obj_list:
        cmds.parent(item, parent, relative=False)


def hierarchical_parent(obj_list):
    """ Parent the objects in hierarchical order

    :param obj_list:
    :return:
    """
    for index, item in enumerate(obj_list):
        if obj_list[index] != obj_list[-1]:
            cmds.parent(obj_list[index], obj_list[index+1])