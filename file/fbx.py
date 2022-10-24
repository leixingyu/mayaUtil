"""
FBX import/export helper module

It is very important to know that the eval command has strict rules on slash
only '/' is allowed, otherwise, fbx import/export will error out

Example:
    preset = "C:/Users/lei/Documents/test.fbximportpreset"
    path = "C:/Users/lei/Documents/test.fbx"
"""

import maya.cmds as cmds
import maya.mel as mel


def reference_fbx(fbx_file, namespace):
    """
    Reference in a .fbx file

    :param fbx_file: str. fbx file to reference in
    :param namespace: str. reference namespace
    :return: str.
    """
    # TODO: return ref nodes
    ref_file = cmds.file(
        fbx_file,
        reference=True,
        type="FBX",
        ignoreVersion=True,
        groupLocator=True,
        mergeNamespacesOnClash=True,
        namespace=namespace,
        options="fbx"
    )
    return ref_file


def export_fbx(nodes, preset_file, export_folder):
    """
    Export specified node as .fbx

    :param nodes: [str]. maya nodes to export
    :param preset_file: str. path to .fbx export preset file
                        use preset instead of setting parameters individually
    :param export_folder: str. export path
    """
    cmds.select(nodes)
    mel.eval('FBXLoadExportPresetFile -f "{}"'.format(preset_file))
    mel.eval('FBXExport -f "{}" -s'.format(export_folder))


def import_fbx(fbx_file, preset_file):
    """
    Import .fbx to scene

    :param fbx_file: str. path to .fbx file
    :param preset_file: str. path to .fbx import preset file
                        use preset instead of setting parameters individually
    :return: [str]. newly imported top nodes from the .fbx
    """
    top_nodes = cmds.ls(assemblies=True)
    mel.eval('FBXLoadImportPresetFile -f "{}"'.format(preset_file))
    mel.eval('FBXImport -f "{}"'.format(fbx_file))
    new_top_nodes = cmds.ls(assemblies=True)

    nodes = [node for node in new_top_nodes if node not in top_nodes]
    return nodes
