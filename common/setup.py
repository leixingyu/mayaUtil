import sys

import maya.cmds as cmds
import maya.mel as mel


def remove_module(module_name):
    """
    Remove module completely to avoid multiple reload

    :param module_name: str. name of the module
    """
    to_delete = list()
    for module in sys.modules:
        if module.split('.')[0] == module_name:
            to_delete.append(module)

    for module in to_delete:
        del(sys.modules[module])


def manage_references():
    """
    Get all reference path according to the reference editor

    :return: list. reference paths
    """
    ref_nodes = cmds.ls(type='reference')
    ref_paths = list()
    for ref_node in ref_nodes:
        try:
            # namespace = cmds.referenceQuery(ref, namespace=1)
            ref_path = cmds.referenceQuery(ref_node, filename=1, shortName=1)
            ref_paths.append(ref_path)
        except:
            pass

    return ref_paths


def unload_references(ref_paths):
    """
    Unload unwanted references

    :param ref_paths: list. reference paths
    """
    for path in ref_paths:
        cmds.file(path, unloadReference=1)


def toggle_layer(layer_sig='*:Layer', is_viz=1):
    """
    Toggle on or off layer

    :param layer_sig: str. pattern used to filter layer, defaults to '*:Layer'
    :param is_viz: bool. visible or not, defaults to 1
    """
    layers = cmds.ls(layer_sig)
    for layer in layers:
        cmds.setAttr('{}.visibility'.format(layer), is_viz)

    cmds.optionVar(intValue=('displayLayerShowNamespace', 1))
    mel.eval('updateLayerEditor')


def load_plugin(name):
    """
    Load plugin if not loaded

    :param name: str. plugin name
    """
    if not cmds.pluginInfo(name, loaded=1, q=1):
        cmds.loadPlugin(name)


def save_preference():
    """
    Save the script editor and default prefs
    """
    # the script editor needs to be open, otherwise tabs will be destroyed
    cmd = '''
    ScriptEditor;
    syncExecuterBackupFiles();
    syncExecuterTabState();
    savePrefs -general;
    '''

    mel.eval(cmd)
