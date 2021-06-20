#!/usr/bin/env python
""" Provide supporting functions for rigging

"""

import maya.cmds as cmds
from .outliner import *

__author__ = "Xingyu Lei"
__maintainer__ = "Xingyu Lei"
__email__ = "wzaxzt@gmail.com"
__status__ = "development"


def get_skin_from_joint(jnt):
    """ get all skinned mesh influenced by certain joint (chain)

    :param jnt: single jnt, preferably jnt root
    :return: list, mesh transform
    """

    cls = cmds.listConnections(jnt, type='skinCluster')
    cls = list(set(cls))

    meshes = []
    for cl in cls:
        meshes += cmds.listConnections(cl, type='mesh')

    return meshes


def get_joint_from_skin(mesh):
    """ get all joints influencing certain skinned mesh

    :param mesh: scene object, could be transform or shape
    :return: list, joints
    """

    if cmds.objectType(mesh, isType='transform'):
        mesh = get_shape_from_transform(mesh)
    elif cmds.objectType(mesh, isType='mesh'):
        pass
    else:
        raise RuntimeError("skin selected is neither transform or mesh type")

    cls = cmds.listConnections(mesh, type='skinCluster')
    jnts = []
    for cl in cls:
        jnt = cmds.listConnections(cl, type='joint')
        jnt = list(set(jnt))
        jnts += jnt

    return jnts


def enable_joint_visibility(roots):
    """ Toggle on joint visibility by all means

    :param roots: joint roots, list or single
    """

    if not isinstance(roots, list):
        roots = [roots]

    for root in roots:
        jnts = get_hierarchy_of_type(root, 'joint')
        for jnt in jnts:
            # visibility
            try:
                cmds.setAttr('{}.v'.format(jnt), lock=0)
                cmds.setAttr('{}.v'.format(jnt), 1)
            except:
                raise RuntimeWarning("channel-box occupied, unable to unlock")

            # draw style
            cmds.setAttr('{}.drawStyle'.format(jnt), 0)

    # model panel joint show
    model_panels = cmds.getPanel(type='modelPanel')
    for model_panel in model_panels:
        cmds.modelEditor(model_panel, e=1, joints=1)

    # TODO: layer toggle on


def orient_joint(jnts):
    """ Orient joint chain exceeding Maya's default behaviour

    :param jnts: list or single
    """

    if type(jnts) == 'list':
        for jnt in jnts:
            cmds.select(jnt, add=True)
    else:
        cmds.select(jnts)
    children = cmds.listRelatives(jnts, children=True, type='joint', ad=True)

    if children:
        cmds.joint(e=True, ch=True, oj='xyz', sao='zup')
        for child in children:
            if cmds.listRelatives(child, children=True, type='joint') is None:
                for attr in ['jointOrientX', 'jointOrientY', 'jointOrientZ']:
                    cmds.setAttr('{}.{}'.format(child, attr), 0)
    else:
        cmds.joint(e=True, oj='xyz', zso=True)  # why zso matters


def clear_joint_orientation(root):
    """ Clear out all joints' rotation to zero but keep weight

    :param root: scene object
    """

    # get all joint orientation from root
    jnts = get_hierarchy_of_type(root, 'joint')

    non_zero_jnts = []
    for jnt in jnts:
        for axis in ['x', 'y', 'z']:
            rot_value = cmds.getAttr('{}.r{}'.format(jnt, axis))
            if rot_value != 0:
                non_zero_jnts.append(jnt)
                break

    for jnt in non_zero_jnts:
        rot_x = cmds.getAttr('{}.rx'.format(jnt))
        rot_y = cmds.getAttr('{}.ry'.format(jnt))
        rot_z = cmds.getAttr('{}.rz'.format(jnt))
        print('non-zero rotation value found in jnt: {}; ' \
              'rotation value: ({},{},{})'.format(jnt, rot_x, rot_y, rot_z))

    # unbind skin, clear rotation, re-bind skin
    meshes = get_skin_from_joint(root)
    cmds.skinCluster(meshes, edit=1, unbindKeepHistory=1)
    jnts = []
    for mesh in meshes:
        jnts += get_joint_from_skin(mesh)
    jnts = list(set(jnts))
    cmds.skinCluster(jnts, meshes)