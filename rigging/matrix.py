"""
Module for Maya transformation matrix

Note:
    om.MTransformationMatrix vs. om.MMatrix
    - om.MTransformationMatrix using MFnTransform only gets local transformation
    matrix, but it stores rotation information greater than 360 degrees
    - om.MMatrix constructed by cmds.xform has access to both local and world
    transformation matrix, but unable to track rotation greater than 360

For math regarding decomposing 4x4 matrices:
https://math.stackexchange.com/questions/237369/
"""

import math

import maya.cmds as cmds
from maya.api import OpenMaya as om


def get_transform_matrix(dag_node):
    """
    Get the local transformation matrix of a given dag node

    :param dag_node: om.MObject. input maya dag node
    :return: om.MTransformationMatrix. local transformation matrix
    """
    fn_transform = om.MFnTransform(dag_node)
    return fn_transform.transformation()


def get_matrix(node, is_world=1):
    """
    Get the transformation matrix of a given maya node in world or object space

    :param node: str. node name
    :param is_world: bool. whether to obtain world space matrix
    :return: om.MMatrix. transformation matrix
    """
    return om.MMatrix(
        cmds.xform(node, q=1, matrix=1, ws=is_world, os=not is_world)
    )


def get_parent_matrix(node):
    """
    Get parent matrix of a maya node
    Parent matrix is used to convert object space transformation matrix to
    world space transformation matrix; this 'offset' matrix will remain the
    same however the object moves.

    Details:
    http://discourse.techart.online/t/convert-world-space-coordinates-to-object-space-coordinates-in-maya/

    world mat = local mat * parent mat
    local mat inverse * world mat = local mat inverse * local mat * parent mat
    parent mat = local mat inverse * world mat

    :param node: str. node name
    :return: om.MMatrix. 'offset' parent matrix
    """
    ws_mat = get_matrix(node)
    ls_mat_inv = get_matrix(node, is_world=0).inverse()

    # the order of matrix multiplication matters
    return ls_mat_inv * ws_mat


def decompose_translation(matrix):
    """
    Decompose translation from a transformation matrix

    Note: om.MMatrix can be converted to om.MTransformationMatrix using
    om.MTransformationMatrix(mmatrix)

    :param matrix: om.MTransformationMatrix. input transformation matrix
    :return: list. vector 3 list representing translation value
    """
    return matrix.translation(om.MSpace.kWorld)


def decompose_rotation(matrix):
    """
    Decompose rotation from a transformation matrix

    Note: om.MMatrix can be converted to om.MTransformationMatrix using
    om.MTransformationMatrix(mmatrix)

    To track angles above 360 degrees, we should avoid converting om.MMatrix
    to om.MTransformationMatrix as it loses this information; instead we
    should obtain the om.MTransformationMatrix from the target node
    https://www.akeric.com/blog/?p=1067

    :param matrix: om.MTransformationMatrix. transformation matrix
    :return: list. vector 3 list representing rotation value
    """
    euler_rot = matrix.rotation().asVector()
    return [math.degrees(angle)
            for angle in (euler_rot.x, euler_rot.y, euler_rot.z)
            ]


def decompose_scale(matrix):
    """
    Decompose scale from a transformation matrix

    Note: om.MMatrix can be converted to om.MTransformationMatrix using
    om.MTransformationMatrix(mmatrix)

    :param matrix: om.MTransformationMatrix. input transformation matrix
    :return: list. vector 3 list representing scale value
    """
    return matrix.scale(om.MSpace.kWorld)
