import os
import time


def get_modify_time(fpath):
    """
    Get file modify time

    :param fpath: str. file path
    :return: int. raw system time
    """
    return time.ctime(os.path.getmtime(fpath))


def get_create_time(fpath):
    """
    Get file creation time

    :param fpath: str. file path
    :return: int. raw system time
    """
    return time.ctime(os.path.getctime(fpath))


def convert_size(size, unit=3):
    """
    Convert the size from bytes to other units like KB, MB or GB

    :param size: int. raw size in bytes
    :param unit: int. output unit
    :return: int. size in converted unit
    """
    class Unit(object):
        BYTES = 1
        KB = 2
        MB = 3
        GB = 4

    if unit == Unit.KB:
        return size / 1024
    elif unit == Unit.MB:
        return size / (1024 * 1024)
    elif unit == Unit.GB:
        return size / (1024 * 1024 * 1024)
    else:
        return size
