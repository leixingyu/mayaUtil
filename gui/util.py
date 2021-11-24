from Qt import QtWidgets, QtGui, QtCore


def is_icon_exists(img):
    """
    Find if file can be displayed in maya shelfButton icon path

    :param img: str. image path in maya shelfButton icon query
    :return: bool. whether icon/image exists
    """
    return QtCore.QFile(img).exists()
