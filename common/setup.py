import sys
from shiboken2 import wrapInstance
from builtins import int

import maya.OpenMayaUI
import maya.cmds as cmds
import maya.mel as mel
from Qt import QtWidgets


def get_maya_main_window():
    """
    Get maya's window instance

    :return: window instance, maya program window
    """
    main_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)


def set_window_pos(child_only=0, x=0, y=0):
    """
    Set window position of maya's widgets

    :param child_only: bool. option to set position only for widgets parented
    to maya main window
    :param x: int. window x position
    :param y: int. window y position
    """
    for child in get_maya_main_window().children():
        if isinstance(child, QtWidgets.QWidget) and child.isWindow():
            # set visible
            if child.isHidden():
                child.setVisible(1)
            child.move(x, y)

    if not child_only:
        tops = QtWidgets.QApplication.topLevelWidgets()
        for top in tops:
            if top.isWindow() and not top.isHidden():
                if top.windowTitle() == get_maya_main_window().windowTitle():
                    continue
                top.move(x, y)


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

    :return: list. reference path
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

    # to unload un-necessary reference
    # for path in ref_discard_paths:
    #    cmds.file(path, unloadReference=1)


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
