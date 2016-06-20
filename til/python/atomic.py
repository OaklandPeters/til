#
#  Atomic
# --------------
# Do you find yourself typechecking for things like is an Iterable but not a String?
# Or is a Sequence, but not a String?
# It is a semi-common practice for Python programmers to define a class very
# similar to 'NonStringIterable' for this purpose, particularly when doing type-dispatching
# during recursive descent down data-structures
# 
# Here is a simpler solution:
import abc
class Atomic(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        """
        If a class has been entered in the register (eg str), then
        this should not trigger.
        """
        if cls is Atomic:
            if not hasattr(subclass, "__iter__"):
                return True
        return NotImplemented

# Numbers and strings are atomic
assert(isinstance(1, Atomic) == True)
assert(isinstance("", Atomic) == True)

# But lists and tuples and dicts are not
assert(isinstance([], Atomic) == False)
assert(isinstance(tuple([]), Atomic) == False)
assert(isinstance({}, Atomic) == False)

# Further, iterators are not Atomic
assert(isinstance(iter([]), Atomic) == False)
assert(isinstance(iter(""), Atomic) == False)