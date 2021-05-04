import os
import shutil

import maya.cmds as cmds


def create_dir(name):
    """ Create a local working directory relative to scene path

    :param name: name of the folder
    :type name: string
    :return: full path of the folder
    :rtype: string
    """

    # local work dir
    scene_fullpath = cmds.file(sceneName=1, q=1)
    scene_path = os.path.dirname(scene_fullpath)

    path = os.path.join(scene_path, name)
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print('directory already exists')

    os.startfile(path)
    print('Created working directory: \n\t{}'.format(path))
    return path


def copy_file(src_path, dst_path):
    """ Copy the file from one place to the other

    :param src_path: source file full path
    :type src_path: string
    :param dst_path: destination folder full path
    :type dst_path: string
    """

    if not os.path.isfile(src_path):
        print('file not located')
        return

    file_name = os.path.basename(src_path)
    if os.path.isfile(os.path.join(dst_path, file_name)):
        print('file already exists in destination directory')
        return

    shutil.copy(src_path, dst_path)
