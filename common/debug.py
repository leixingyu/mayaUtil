import maya.cmds as cmds


def pprint_attr_shortname(mobject):
    """
    Debug maya object attribute short names

    :param mobject: str. maya node
    """
    longs = [i for i in cmds.listAttr(mobject)]
    shorts = [i for i in cmds.listAttr(mobject, sn=1)]

    if len(longs) != len(shorts):
        return

    for i in range(len(longs)):
        print('{}: {}'.format(longs[i], shorts[i]))


def get_loaded_plugins(is_auto=False):
    """
    Get loaded plugin in current maya session

    :param is_auto: bool. filter auto loaded plugins
    :return: list. full path of the plugin
    """
    plugins = cmds.pluginInfo(query=1, listPlugins=1, autoload=is_auto)
    return [cmds.pluginInfo(p, query=1, path=1) for p in plugins]

