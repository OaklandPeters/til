"""
This has not been made into a TIL in til/python yet, because...
it does not work correctly atm.

However, I'm reasonably sure I can get it to work (since I've got type-level operatores to work in the past)

"""


#
# Class-level operators
#--------------------------
# Requires metaclasses
# To make this work with instance-level overrides is complicated
# ... I should look to the proper method lookup, as described here:
# https://blog.ionelmc.ro/2015/02/09/understanding-python-metaclasses/
# 
# ... actually, I'm pretty sure I need to use something like my @pedanticmethod
# to make __mul__ work as both a classmethod and instancemethod
class OperatorMeta(type):
    def __mul__(cls, other):
        if hasattr(cls, '__mul__'):
            return cls.__mul__(other)
        else:
            return type.__mul__(cls, other)
            raise TypeError(str.format(
                "unspported operand type(s) for *: '{0}' and '{1}'",
                cls.__name__, type(other).__name__
            ))

class ThreeBase(metaclass=OperatorMeta):
    base = 3
    @classmethod
    def __mul__(cls, value):
        return cls.base * value
    def __init__(self, base):
        self.base = base

assert((ThreeBase * 5) == 15)
assert((ThreeBase(10) * 5) == 50 )  # WRONG. Still returns 15
# This does not work correctly, the problem being I forget how
# to make OperatorMeta.__mul__ proxy down to the instance level
# ... HOWEVER, if I look up the standard rules for method lookup,
# in relation to metaclasses (the standard metaclass being 'type')
# then that should show me what to do
