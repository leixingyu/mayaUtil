import logging

import maya.cmds as cmds
from maya.api import OpenMaya as om
from pipelineUtil.common import algorithm

from ..common import dag, hierarchy


def merge_curves(name, curves=None):
    """
    Merge separate nurbs curve under one transform for easy selection

    :param name: str. parent node name
    :param curves: list. list of curve transforms
    :return: str. transform node
    """
    # by default, selection in viewport are transform nodes
    if not curves:
        curves = cmds.ls(selection=1)

    for curve in curves:
        if cmds.nodeType(curve) != 'transform':
            logging.error('Merge fail, %s not transform node', curve)
            return 0

    shapes = list()
    for xform in curves:
        shape = hierarchy.get_shape_from_xform(
            xform,
            check_unique_child=0
        )
        cmds.makeIdentity(xform, apply=1, r=1, t=1, s=1)
        shapes.extend(shape)

    parent = cmds.createNode('transform', n=name)
    cmds.parent(shapes, parent, s=1, r=1)
    # delete the make curves node
    cmds.delete(parent, constructionHistory=1)
    # delete the empty parent
    cmds.delete(curves)

    return parent


def make_curve_by_text(text, name, font='MS Gothic'):
    """
    Make a controller out of text

    :param text: str. the text used for generate controller shape
    :param name: str. name of the controller
    :param font: str. font used for the text
    :return: str. controller transform
    """
    temp = cmds.group(em=1)

    curve = cmds.textCurves(text=text, font=font)
    curve_shapes = cmds.listRelatives(curve, ad=1)
    for shape in curve_shapes:
        if cmds.nodeType(shape) == 'nurbsCurve':
            cmds.parent(shape, temp, absolute=1, shape=1)
    cmds.delete(curve)

    curve_shapes = cmds.listRelatives(temp, children=1)
    for xform in curve_shapes:
        cmds.makeIdentity(xform, apply=1, t=1, r=1, s=1)
    merge_curves(name, curves=curve_shapes)
    cmds.delete(temp)

    return name


def get_point_on_curve(curve, sample):
    """
    Get point info on nurbs curve with uniform distance
    https://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__cpp_ref_class_m_fn_nurbs_curve_html

    :param curve: str. nurbs curve name
    :param sample: int. how many points to sample
    :return: tuple. om.MPoint object and om.MVector object
    """
    plists = algorithm.get_percentages(sample)

    points = list()
    tangents = list()
    crv_fn = om.MFnNurbsCurve(dag.get_dag_path(curve))
    for percentage in plists:
        parameter = crv_fn.findParamFromLength(crv_fn.length() * percentage)
        point = om.MPoint()
        crv_fn.getPointAtParam(parameter, point)
        tangent = crv_fn.tangent(parameter)

        points.append(point)
        tangents.append(tangent)

    return points, tangents
