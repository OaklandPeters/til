#   Copy Semantics
# -------------------------
# Copy vs deep-copy, and what they do
# In short: copy is a pointer, and deep-copy is an entirely seperate data structure.
# BUT.... this behavior is inconsistent, because of the way that attribute
#   setters work in Python.
#   Thus, mutations of attributes is not shared with copies, but mutations
#   of items IS shared.
# See example #1 VS #2
import copy

# Example #1
# Item mutation DOES change copies, but not deep copies
original = ["one", "two", ["three", "333"]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)
assert (original == shallow)
assert (original == deep)
assert (shallow == deep)
original[2][0] = "four"
assert (original == shallow)
assert (original != deep)
assert (shallow != deep)

# Example #2
# Attribute mutation does not change copies, nor deep copies
class Person:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.name)
    def __eq__(self, other):
        return self.name == other.name

original = Person("Ulysses")
shallow = copy.copy(original)
deep = copy.deepcopy(original)

assert (original == shallow)
assert (original == deep)
assert (shallow == deep)

original.name = "Grant"
assert (original != shallow)
assert (original != deep)
assert (shallow == deep)
