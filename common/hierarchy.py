import maya.cmds as cmds


def get_root_node(obj, type_specified=None):
    """
    Get the root of the object in the hierarchy

    :param obj: str. scene object
    :param type_specified: str. restrict the root node type
    :return: str. the root scene object
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


def get_all_under_hierarchy(root):
    """
    Get all children in the hierarchy of a root (excluding the root)

    :param root: str. single scene object
    :return: list. children and grand children of the root
    """
    children = list()
    direct_children = cmds.listRelatives(root, children=1)
    if direct_children:
        children.extend(direct_children)
        for child in direct_children:
            children.extend(get_all_under_hierarchy(child))
    return children


def get_hierarchy_of_type(root, type_specified):
    """
    Get all children (excluding root) in hierarchy of a certain type

    :param root: str. single scene object
    :param type_specified: str. object type
    :return: list. object of the specified type
    """
    children = get_all_under_hierarchy(root)
    return cmds.ls(children, type=type_specified)


# TODO: combine the following two functions into one
def delete_hierarchy_except_type(roots, type_specified):
    """
    Delete all other types of objects under hierarchy of root
    note: the function cannot re-parent shape node to another transform
    but since it is always on top, it is safe to delete before hand

    :param roots: list or str. scene obj
    :param type_specified: str. object type
    """
    if not isinstance(roots, list):
        roots = [roots]

    for root_obj in roots:
        children = cmds.listRelatives(root_obj, children=1)
        if not children:
            # the current object is at top
            if not cmds.objectType(root_obj, isType=type_specified):
                cmds.delete(root_obj)
        else:
            # the current object has children
            for child in children:
                # the child is not top object or different type, re-parent
                if not cmds.objectType(root_obj, isType=type_specified):
                    cmds.parent(child, cmds.listRelatives(root_obj, parent=1))
                delete_hierarchy_except_type(child, type_specified)

            # children moved under another parent, delete original parent
            if not cmds.objectType(root_obj, isType=type_specified):
                cmds.delete(root_obj)


def delete_hierarchy_except_node(roots, type_specified):
    """
    Delete all other types of objects under hierarchy of root
    note: the function cannot re-parent shape node to another transform
    but since it is always on top, it is safe to delete before hand

    :param roots: list or str. scene obj
    :param type_specified: str. object type
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
                    cmds.parent(
                        child,
                        cmds.listRelatives(root_obj, parent=1)
                    )
                delete_hierarchy_except_node(child, type_specified)

            # children moved under another parent, delete original parent
            if not cmds.listConnections(root_obj, type=type_specified):
                cmds.delete(root_obj)


def delete_hierarchy_shape(roots):
    """
    Delete all shapes under the given root

    :param roots: list or str. scene object
    """
    if not isinstance(roots, list):
        roots = [roots]

    for root in roots:
        nodes = cmds.listRelatives(root, ad=1)
        shapes = cmds.ls(nodes, shapes=1)
        if shapes:
            cmds.delete(shapes)


def get_shape_from_transform(
        transform,
        enable_result_only=1,
        check_unique_child=1):
    """
    Get shape nodes under the transform

    :param transform: str. single scene object
    :param enable_result_only: bool. get only the result shape
    :param check_unique_child: bool. check if transform has multiple shapes
    :return: list. the shape node
    """
    shapes = cmds.listRelatives(transform, shapes=1)
    shapes_result = [shape for shape in shapes if 'Orig' not in shape]

    if check_unique_child:
        assert len(shapes_result) != 0, "no shape node found"
        assert len(shapes_result) == 1,\
            "multiple shape node found in {} they are: {}" .format(
                transform,
                str(shapes_result)
            )

    if enable_result_only:
        return shapes_result
    else:
        return shapes


def batch_parent(obj_list, parent):
    """
    Grouping multiple objects to the same parent

    :param obj_list: list, children objects
    :param parent: str. parent object
    """
    for item in obj_list:
        cmds.parent(item, parent, relative=0)


def hierarchical_parent(obj_list):
    """
    Parent the objects in hierarchical order

    :param obj_list: objects to parent in order
    """
    for index, item in enumerate(obj_list):
        if obj_list[index] != obj_list[-1]:
            cmds.parent(obj_list[index], obj_list[index+1])
