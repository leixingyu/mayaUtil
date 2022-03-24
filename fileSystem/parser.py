"""

f = 'D:\\testbin\\maya-file.ma'
ma = MayaAscii(f)

with open("C:\Users\\Lei\\Downloads\\output.txt", "w") as file:
    file.write(ma.diagnose_usage())

"""

from .mayaAsciiNode import MayaAsciiNode


def diagnose_usage(path):
    output = ''

    # sort
    nodes = MayaAsciiNode.from_file(path)
    nodes = sorted(nodes, key=lambda n: n.size, reverse=1)

    for node in nodes:
        # filter
        if node.percent < 0.1:
            continue

        line = "[line: {index}][{size} mb][{percent}%] {description} \n".format(
            index=node.index,
            description=node.description,
            percent=node.percent,
            size=round(node.size / float(1024) / float(1024), 4)
        )
        output += line

    return output
