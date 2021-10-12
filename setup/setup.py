from shiboken2 import wrapInstance
from builtins import int

from utility._vendor.Qt import QtWidgets

import maya.OpenMayaUI
import maya.cmds as cmds
import maya.mel as mel


def get_maya_main_window():
    """ Get the window instance of Maya

    :return: window instance, maya program window
    """

    main_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)


def set_window_pos(child_only=False, x=0, y=0):
    """ Set window position of maya's widgets

    :param child_only: option to set position only for widgets parented
    to maya main window, defaults to False
    :type child_only: bool, optional
    :param x: window x position, defaults to 0
    :type x: int, optional
    :param y: window y position, defaults to 0
    :type y: int, optional
    """

    for child in get_maya_main_window().children():
        if isinstance(child, QtWidgets.QWidget) and child.isWindow():
            # set visible
            if child.isHidden():
                child.setVisible(True)
            child.move(x, y)

    if not child_only:
        tops = QtWidgets.QApplication.topLevelWidgets()
        for top in tops:
            if top.isWindow() and not top.isHidden():
                if top.windowTitle() == get_maya_main_window().windowTitle():
                    continue
                top.move(x, y)


def remove_module(module_name):
    """ Remove module completely to avoid multiple reload

    :param module_name: string
    """
    import sys
    print('Removing {} module'.format(module_name))

    to_delete = []
    for module in sys.modules:
        if module.split('.')[0] == module_name:
            to_delete.append(module)

    for module in to_delete:
        del(sys.modules[module])


def manage_references():
    """ get all reference path according to the reference editor

    :return: reference path
    :rtype: list of strings
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


def toggle_layer(layer_sig='*:Layer', is_viz=True):
    """ Toggle on or off layer

    :param layer_sig: pattern used to filter layer, defaults to '*:Layer'
    :type layer_sig: str, optional
    :param is_viz: visible or not, defaults to True
    :type is_viz: bool, optional
    """

    layers = cmds.ls(layer_sig)
    for layer in layers:
        cmds.setAttr('{}.visibility'.format(layer), is_viz)

    cmds.optionVar(intValue=('displayLayerShowNamespace', 1))
    mel.eval('updateLayerEditor')


def load_plugin(name):
    """ load plugin if not loaded

    :param name: plugin name
    :type name: string
    """
    if not cmds.pluginInfo(name, loaded=1, q=1):
        cmds.loadPlugin(name)


def save_preference():
    """
    Save the script editor and default prefs
    """

    # the script editor needs to be open, otherwise tabs will be destoried
    cmd = '''
    ScriptEditor;
    syncExecuterBackupFiles();
    syncExecuterTabState();
    savePrefs -general;
    '''

    mel.eval(cmd)
