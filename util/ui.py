from utility._vendor.Qt import QtWidgets


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
