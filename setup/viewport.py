from functools import wraps

import maya.cmds as cmds

PANE_NAME = 'viewPanes'  # also known as $gMainPane in mel
RENDERER = 'vp2Renderer'


def get_model_panels():
    """
    Get the current model panels in the viewport

    :return: list. model panel names
    """
    panels = cmds.getPanel(vis=1)
    model_panels = [panel
                        for panel in panels
                            if cmds.getPanel(typeOf=panel) == 'modelPanel']

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


def viewport_off(func):
    """
    src: https://blog.asimation.com/disable-maya-viewport-while-running-code/
    Decorator - turn off Maya display while func is running.
    if func will fail, the error will be raised after.
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        cmds.paneLayout(PANE_NAME, manage=0, edit=1)
        try:
            return func(*args, **kwargs)
        except Exception:
            # will raise original error
            raise
        finally:
            cmds.paneLayout(PANE_NAME, manage=1, edit=1)
    return wrap
