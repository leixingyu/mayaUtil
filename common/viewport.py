import os

import maya.cmds as cmds

PANE_NAME = 'viewPanes'  # also known as $gMainPane in mel
RENDERER = 'vp2Renderer'


def get_model_panels():
    """
    Get the current model panels in the viewport

    :return: list. model panel names
    """
    panels = cmds.getPanel(vis=1)
    model_panels = [
        panel for panel in panels
        if cmds.getPanel(typeOf=panel) == 'modelPanel'
    ]

    return model_panels


def show_polymesh_only(model_panels=None):
    """
    Hide everything except for polymesh for current model panels

    :param model_panels: list. model panels, defaults to None
    """
    if not model_panels:
        model_panels = get_model_panels()

    for model_panel in model_panels:
        cmds.modelEditor(model_panel, allObjects=0, polymeshes=1, e=1)


def switch_renderer(renderer, model_panels=None):
    """
    Switch renderer of the current model panels

    :param renderer: str. renderer name
    :param model_panels: list. model panels
    """
    if not model_panels:
        model_panels = get_model_panels()

    for model_panel in model_panels:
        if renderer in cmds.modelEditor(model_panel, rendererList=1, q=1):
            cmds.modelEditor(model_panel, rendererName=renderer, e=1)


def switch_camera(camera, model_panels=None):
    """
    Switch camera of the current model panels

    :param camera: str. camera name
    :param model_panels: list. model panels
    """
    if not model_panels:
        model_panels = get_model_panels()

    cameras = cmds.ls(type='camera')
    if camera in cameras:
        for model_panel in model_panels:
            cmds.modelEditor(model_panel, camera=camera, e=1)


def take_maya_screenshot(path, name):
    """
    Take a screenshot in maya viewport
    :param path: str. output directory
    :param name: str. name of the screenshot
    :return: str. full path to the screenshot
    """
    file_name = '{}.jpg'.format(name)
    full_path = os.path.join(path, file_name)

    if cmds.ls(selection=1):
        cmds.select(clear=1)
        cmds.selectMode(object=1)

    cmds.viewFit()
    cmds.setAttr('defaultRenderGlobals.imageFormat', 8)
    cmds.playblast(
        completeFilename=full_path,
        st=1,
        et=1,
        format='image',
        forceOverwrite=1,
        w=600,
        h=600,
        showOrnaments=0,
        viewer=0
    )

    return full_path
