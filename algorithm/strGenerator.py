import random
import string


class StrGenerator(object):

    def __init__(self, prefix='', length=6):

        self._prefix = prefix
        self._len = length

        self._choices = string.ascii_uppercase+string.digits

    @staticmethod
    def get_random_string(choices, length):

        return ''.join(random.choice(choices) for _ in range(length))

    @property
    def tmp(self):
        choices = string.ascii_lowercase+string.digits
        return self._prefix + self.get_random_string(choices, self._len)