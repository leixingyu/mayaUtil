import maya.cmds as cmds


def inspect():
    return get_unknown_plugin()


def fix_selected(node):
    delete_unknown_plugin(node)


def fix_all(nodes):
    for plugin in nodes:
        delete_unknown_plugin(plugin)


def get_unknown_plugin():
    """
    Get unknown plugin in the scene

    :return: list. names of the unknown plugins
    """
    return cmds.unknownPlugin(q=1, l=1)


def delete_unknown_plugin(plugin):
    """
    Delete given unknown plugins

    :param plugin: str. name of the unknown plugins
    """
    cmds.unknownPlugin(plugin, remove=1)

