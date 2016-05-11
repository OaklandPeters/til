"""
This file is a companion to simple_list.md - and is intended to be an 
importable module.
"""


class List:
    """
    """
    def __init__(self, values=None):
        if values is None:
            self.values = []
        else:
            self.values = [elm for elm in values]

    def __iter__(self):
        return iter(self.values)

    #-----------------------------------
    #    Monoid functions
    #-----------------------------------
    @classmethod
    def zero(cls):
        return cls()

    def append(self, other):
        return type(self)([elm for array in (self, other) for elm in array])

    def join(self):
        cls = type(self)
        accumulator = cls.zero()
        for elm in self:
            if isinstance(elm, cls):
                accumulator = accumulator.append(elm)
            else:
                accumulator = accumulator.append(cls([elm]))
        return accumulator

    #-----------------------------------
    #    Functor-related
    #-----------------------------------
    def map(self, function):
        return type(self)(function(elm) for elm in self)

    def bind(self, function):
        return self.map(function).join()

    @classmethod
    def _traverse(cls, elm, function):
        if isinstance(elm, cls):
            return elm.traverse(function)
        else:
            return function(elm)
    
    def traverse(self, function):
        # return type(self)(self._traverse(elm, function) for elm in self)
        return type(self)(self.map(lambda elm: self._traverse(elm, function)))

    #-----------------------------------
    #    Additional functional utility
    #-----------------------------------
    def filter(self, function):
        return type(self)(elm for elm in self if function(elm))

    @classmethod
    def recurse(cls, function):
        def wrapper(element):
            if isinstance(element, cls):
                return wrapper(element)
            else:
                return function(element)
        return wrapper

    #---------------------------------------------
    #  Python magic methods 
    #     Makes this into a representable,
    #     comparable, Sequence
    #-----------------------------------------
    def __len__(self):
        return len(self.values)

    def __contains__(self, value):
        return value in self.values

    def __getitem__(self, index):
        return self.values[index]

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        elif len(self) != len(other):
            return False
        else:
            for left, right in zip(self, other):
                # This step may recurse when left is a List
                if left != right:
                    return False
            return True

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return str.format(
            "{0}[{1}]",
            self.__class__.__name__,
            ", ".join(repr(elm) for elm in self)
        )

    #------------------------------------------------
    #   Python list functions
    #------------------------------------------------
    def index(self, value):
        return self.values.index(value)
