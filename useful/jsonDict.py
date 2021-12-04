"""
Helper class for dealing with json file similar to dictionary, to use:

f1 = r"D:/testbin/json/test.json"
f2 = r"D:/testbin/json/test2.json"
data = {
    'a': 1,
    'b': [2, 3],
    'c': {
        'd': 4
    }
}

# read
d0 = JsonDict(data)
d1 = JsonDict.from_json(f1)

# used it normally like dictionary
print d1.keys(), d1.values(), d1.items()
d1['test'] = 'hello'
d1.pop('a')

# write
d1.to_json(f2)
print type(d1.to_dict())
"""

import json
from collections import OrderedDict


class JsonDict(OrderedDict):
    def __init__(self, data):
        super(JsonDict, self).__init__(data)

    @classmethod
    def from_json(cls, path):
        with open(path) as input_file:
            try:
                data = json.load(input_file, object_pairs_hook=OrderedDict)
                if data:
                    return cls(data)
            except:
                pass

    def to_json(self, path):
        with open(path, 'w') as out_file:
            try:
                json.dump(self, out_file, indent=4, ensure_ascii=False)
            except TypeError:
                # if the json file is blank, a type error will raise
                # TypeError was not handled: "must be unicode, not str"
                pass

    def to_dict(self):
        return dict(self)
