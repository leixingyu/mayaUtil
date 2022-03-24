from collections import namedtuple

from .mayaAscii import MayaAscii


AsciiBase = namedtuple('AsciiBase', ['ascii', 'index', 'description', 'size'])


class MayaAsciiNode(AsciiBase):
    __slots__ = ()

    def __new__(
        cls,
        ascii,
        index,
        description='',
        size=0
    ):
        return super(MayaAsciiNode, cls).__new__(cls, ascii, index, description, size)

    @classmethod
    def from_file(cls, path):
        nodes = list()

        with open(path) as f:
            ascii = MayaAscii(path)

            prv_index = -1
            prv_description = ''
            prv_size = 0

            for index, line in enumerate(f):
                if not line:
                    continue

                # a node doesn't have any indentation
                # whereas the node's attributes are all indented
                # the last node is ignored as it indicates end of file
                if not line.startswith('\t'):
                    node = cls(ascii, prv_index, prv_description, prv_size)

                    prv_index = index + 1
                    prv_description = line
                    prv_size = len(line)

                    nodes.append(node)
                else:
                    prv_size += len(line)

        return nodes

    @property
    def percent(self):
        percent = self.size / float(self.ascii.size) * 100
        return round(percent, 5)
