import random
import string


class StrGenerator(object):
    """
    A temporary string generator for purpose like creating temp name
    s = StrGenerator()
    temp_string = s.tmp
    """

    def __init__(self, prefix='', length=6):
        """
        :param prefix: str. prefix before randomize string
        :param length: int. length of string
        """
        self._prefix = prefix
        self._len = length
        self._choices = string.ascii_uppercase + string.digits

    @property
    def tmp(self):
        """
        Get finalized randomized string with prefix

        :return: str.
        """
        return self._prefix + get_random_string(self._choices, self._len)


def get_random_string(choices, length):
    """
    Get randomize string based on option

    :param choices: (). pattern of the random generated string
    :param length: int. length of string
    :return: str.
    """
    return ''.join(random.choice(choices) for _ in range(length))
