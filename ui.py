from Qt import QtWidgets

# TODO: confirm the following


def set_export_path(title='Export', default_path='C:/', file_type='*'):
    """ Get directory/folder full path for export

    :param title: export window title, defaults to 'Export'
    :type title: str, optional
    :param default_path: default path opened in the window
    :type default_path: string
    :param file_type: file filter pattern
    :type file_type: string
    :return: export folder full path
    :rtype: string
    """

    path = QtWidgets.QFileDialog.getSaveFileName(
        None,
        title,
        default_path,
        filter=file_type)[0]

    return path


def set_import_path(title='Import', default_path='C:/', file_type='*'):
    """ Get file full path for export

    :param title: import window title, defaults to 'Import'
    :type title: str, optional
    :param default_path: default path opened in the window
    :type default_path: string
    :param file_type: file filter pattern
    :type file_type: string
    :return: import file full path
    :rtype: string
    """

    path = QtWidgets.QFileDialog.getOpenFileName(
        None,
        title,
        default_path,
        filter=file_type)[0]

    return path
