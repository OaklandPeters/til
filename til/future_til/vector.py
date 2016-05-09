from UserList import UserList
from pprint import pformat

class Vector(UserList, object):
    """Simple accumulator object, giving vectorized method access."""
    def __init__(self, sequence):
        self.data = sequence

    def apply(self, func):
        """This is all the magic. Seriously."""
        return type(self)([func(elm) for elm in self.data])

    def __getattr__(self, name):
        """Only tiggers when this class is missing an attribute.
        IE all of the vectorized method access hits this."""
        # return type(self)([getattr(elm, name) for elm in self.data])
        return self.apply(lambda elm: getattr(elm, name))

    def __repr__(self):
        """Mark that this is a Vector object, before showing data."""
        return "{0}({1})".format(type(self).__name__, [repr(elm) for elm in self.data])

    def __getitem__(self, index):
        """Handle slices"""
        if isinstance(index, slice):
            return type(self)(super(Vector, self).__getitem__(index))
        else:
            return type(self)([super(Vector, self).__getitem__(index)])
    
    def __call__(self, *args, **kwargs):
        """Handle callables"""
        return self.apply(lambda elm: elm(*args, **kwargs))

    def pretty(self):
        return pformat(self.data, indent=4)
