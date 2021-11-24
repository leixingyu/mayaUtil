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
