from maya.api import OpenMaya as om


def get_dg_path(node=None):
    """
    Get DAG path of the specified node

    :param node: str. maya node
    :return: MDagPath. Dag path of the maya node
    """
    selection = om.MSelectionList()
    selection.add(node)
    dag_path = om.MDagPath()
    selection.getDagPath(0, dag_path)
    return dag_path


def print_dg_children(dg_path):
    """
    Debug all the children's Dag path
    
    :param dg_path: MDagPath. parent Dag path
    """
    dag_iter = om.MItDag(om.MItDag.kBreadthFirst)
    dag_iter.reset(dg_path)
    while not dag_iter.isDone():
        path = om.MDagPath()
        dag_iter.getPath(path)
        print path.fullPathName()
        dag_iter.next()


def get_dg_node(node=None):
    """
    Get Dependency Graph Node of the specified maya node

    :param node: str. maya node
    :return: MObject. MObject of the maya node
    """
    selection = om.MSelectionList()
    selection.add(node)
    mobject = om.MObject()
    selection.getDependNode(0, mobject)
    return mobject


def traverse_dg_node_type(mobject, direction, dgtype):
    """
    Get all DG node of type by traversing the node network

    @param mobject: MObject. maya DG node to traverse
    @param direction: MItDependencyGraph.Direction. traversal direction
    @param dgtype: MFn.Type. type of the DG node

    @return: list. all DG node of type
    """
    # Create a dependency graph iterator for our current object
    # this could also be plug level
    dg_iter = om.MItDependencyGraph(
        mobject,
        direction,
        om.MItDependencyGraph.kNodeLevel
    )

    # find the first match type
    names = list()
    while not dg_iter.isDone():
        current = dg_iter.currentItem()
        node_funcs = om.MFnDependencyNode(current)
        if current.hasFn(dgtype):
            name = node_funcs.name()
            names.append(name)

        dg_iter.next()

    return names
