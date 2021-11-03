import logging

import maya.cmds as cmds
from maya import OpenMaya as om

from utility.setup import outliner
from utility.util import other
from utility.algorithm import algorithm


def colorize_rgb(crv, r, g, b):
    """
    Colorize the nurbs curve

    :param crv: str. nurbs curve
    :param r: float. red channel value
    :param g: float. green channel value
    :param b: float. blue channel value
    """

    colorize_rgb_normalized(crv, r/255.0, g/255.0, b/255.0)


def colorize_rgb_normalized(crv, r, g, b):
    """
    Colorize the nurbs curve

    :param crv: str. nurbs curve
    :param r: float. normalized red channel value
    :param g: float. normalized green channel value
    :param b: float. normalized blue channel value
    """
    if cmds.nodeType(crv) != 'transform':
        return

    cmds.setAttr('{}.overrideEnabled'.format(crv), 1)
    cmds.setAttr('{}.overrideRGBColors'.format(crv), 1)
    cmds.setAttr('{}.overrideColorRGB'.format(crv), r, g, b)


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
            return False

    shapes = []
    for transform in curves:
        shape = outliner.get_shape_from_transform(transform, check_unique_child=0)
        cmds.makeIdentity(transform, apply=1, r=1, t=1, s=1)
        shapes.extend(shape)

    parent = cmds.createNode('transform', n=name)
    cmds.parent(shapes, parent, s=1, r=1)
    cmds.delete(parent, constructionHistory=1)

    return parent


def make_curve_by_text(text, name, font='MS Gothic'):
    """
    Make a controller out of text

    :param text: str. the text used for generate controller shape
    :param name: str. name of the controller
    :param font: str. font used for the text
    :return: str. controller transform
    """

    temp = cmds.group(em=True)
    ctrl = cmds.group(em=True, name=name)

    curve = cmds.textCurves(text=text, font=font)
    curve_shapes = cmds.listRelatives(curve, ad=True)
    for shape in curve_shapes:
        if cmds.nodeType(shape) == 'nurbsCurve':
            cmds.parent(shape, temp, absolute=True, shape=True)
    cmds.delete(curve)

    curve_shapes = cmds.listRelatives(temp, children=True)
    for transform in curve_shapes:
        cmds.makeIdentity(transform, apply=True, t=1, r=1, s=1)

    curve_shapes = cmds.listRelatives(temp, ad=True)
    for shape in curve_shapes:
        if cmds.nodeType(shape) == 'nurbsCurve':
            cmds.parent(shape, ctrl, relative=True, shape=True)
    cmds.delete(temp)
    cmds.select(clear=True)

    return ctrl


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
    crv_fn = om.MFnNurbsCurve(other.get_dag_path(curve))
    for percentage in plists:
        parameter = crv_fn.findParamFromLength(crv_fn.length() * percentage)
        point = om.MPoint()
        crv_fn.getPointAtParam(parameter, point)
        tangent = crv_fn.tangent(parameter)

        points.append(point)
        tangents.append(tangent)

    return points, tangents
