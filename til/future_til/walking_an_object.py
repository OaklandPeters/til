#
# Walking an object
#--------------------
# A recursive descent iterator for walking down an object
class Pathstring(list):
    def __str__(self):
        return ".".join(self)

    def __add__(self, other):
        return self.extend(other)
    
def walk(obj, path=None):
    if path is None:
        path = tuple()
    else:
        yield Pathstring(path)

    if len(path) >= 10:
        return
    if not hasattr(obj, '__dict__'):
        return
    for key, value in vars(obj).items():
        for _path in walker(value, path=path+(key,)):
            yield Pathstring(_path)

def obj_get(obj, path):
    """get attribute path as a reduction"""
    accumulator = obj
    for step in path:
        accumulator = getattr(accumulator, step)
    return accumulator

def obj_items(obj, outer_path=None):
    """Walk item, and return (path, value) pairs, similar to (key, value)
    pairs from dict.items()"""
    for path in walk(myobj, tuple(['myobj'])):
        yield (path, obj_get(obj, path[1:]))

class MyClass(object):
    pass
myobj = MyClass()

myobj.left = dict()
myobj.right = "asdlfkasj"
myobj.middle = dict

for path in walk(myobj):
    print(path)