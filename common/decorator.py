from functools import wraps

import maya.cmds as cmds

from .viewport import PANE_NAME


def undo_actions(func):
    """
    Undo series of maya actions
    """
    @wraps(func)
    def _undofunc(*args, **kwargs):
        try:
            # start an undo chunk
            cmds.undoInfo(ock=1)
            return func(*args, **kwargs)
        finally:
            # after calling the func, end the undo chunk and undo
            cmds.undoInfo(cck=1)
            cmds.undo()

    return _undofunc


def viewport_off(func):
    """
    Turn off maya viewport display
    src: https://blog.asimation.com/disable-maya-viewport-while-running-code/
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


def maya_timed(func):
    """
    Time function using maya timer
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        cmds.timer(startTimer=1)
        try:
            func(*args, **kwargs)
        except Exception:
            raise
        finally:
            print('total execution time: {}s'.format(cmds.timer(e=1)))
    return wrap
