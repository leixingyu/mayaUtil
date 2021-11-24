from Qt import QtWidgets, QtGui, QtCore


def pick_color(qcolor=None):
    """
    Prompt user to pick a color

    :param qcolor: QtGui.QColor. pre-selected color
    :return: QtGui.QColor. user selected color
    """
    if not qcolor:
        qcolor = QtGui.QColor(0, 0, 0)

    return QtWidgets.QColorDialog.getColor(qcolor)


def set_export_path(title='Export', default_path='C:/', file_type='*'):
    """
    Get directory/folder full path for export

    :param title: str. export window title, defaults to 'Export'
    :param default_path: str. default path opened in the window
    :param file_type: str. file filter pattern
    :return: str. export folder full path
    """
    path = QtWidgets.QFileDialog.getSaveFileName(
        None,
        title,
        default_path,
        filter=file_type)[0]
    return path


def set_import_path(title='Import', default_path='C:/', file_type='*'):
    """
    Get file full path for export

    :param title: str. import window title, defaults to 'Import'
    :param default_path: str. default path opened in the window
    :param file_type: str. file filter pattern
    :return: str. import file full path
    """
    path = QtWidgets.QFileDialog.getOpenFileName(
        None,
        title,
        default_path,
        filter=file_type)[0]
    return path


def message_log(message, ltype='error', title=''):
    """
    Activate a message box prompt with one confirm button

    :param message: str. custom message
    :param ltype: str ('error' or 'info'). type of the log
    :param title: str. message box title
    :return: widget instance
    """
    icon = None
    if ltype == 'error':
        icon = QtWidgets.QMessageBox.Critical
    elif ltype == 'info':
        icon = QtWidgets.QMessageBox.Information

    msg_box = QtWidgets.QMessageBox()

    msg_box.setIcon(icon)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)

    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    return msg_box.exec_()


def message_yesno(message, title=''):
    """
    Raise a message box prompt for user to choose

    :param message: str. custom message
    :param title: str. message box title
    :return: QtWidgets.QMessageBox.Yes or No. user's choice
    """
    msg_box = QtWidgets.QMessageBox()

    msg_box.setIcon(QtWidgets.QMessageBox.Question)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)

    msg_box.setStandardButtons(
        QtWidgets.QMessageBox.Yes |
        QtWidgets.QMessageBox.No)
    user_choice = msg_box.exec_()
    return user_choice
