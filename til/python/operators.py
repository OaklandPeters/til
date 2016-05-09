"""
Different take on operator.py library.
"""
import abc
import operator

class Operator:
    symbol = NotImplemented
    function = NotImplemented

    def __init__(self, symbol, function):
        self.symbol = symbol
        self.function = function

    def __new__(cls, *args, **kwargs):
        return cls.__call__(*args, **kwargs)

    def __str__(self):
        return str(self.symbol)

    def __repr__(self):
        return "<Operator {0}>".format(self.__class__.__name__)

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


NotEqual = Operator("!=", operator.__ne__)
Equal = Operator("==", operator.__eq__)
Greater = Operator(">", operator.__gt__)
GreaterEqual = Operator(">=", operator.__ge__)
Less = Operator("<", operator.__lt__)
LessEqual = Operator("<=", operator.__le__)

IsInstance = Operator("isinstance", isinstance)
IsSubclass = Operator("issubclass", issubclass)
