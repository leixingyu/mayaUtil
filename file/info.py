import os
import time


def get_modify_time(path):
    return time.ctime(os.path.getmtime(path))


def get_create_time(path):
    return time.ctime(os.path.getctime(path))


def convert_size(size, unit=3):
    """
    Convert the size from bytes to other units like KB, MB or GB
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
