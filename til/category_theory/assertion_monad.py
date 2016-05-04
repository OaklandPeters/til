class Assertion:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.value)

    @classmethod
    def lift(cls, value):
        return cls(value)

    def apply(self, function, message=None):
        result = function(self.value)
        if not result:
            if callable(message):
                _message = message(self.value)
            elif isinstance(_message, str):
                _message = message
            elif message is None:
                _message = str.format(
                    "It is not true that: {0} ({1})",
                    function.__name__,
                    self.value
                )
            else:
                raise ValueError("Invalid argument 'message'.")
            raise AssertionError(_message)

    def bind(self, function):
        return self.lift(function(self.value))

    #
    #
    #
    def __ne__(self, other):
        return self.apply(lambda value: value != other)

    def __eq__(self, other):
        return self.apply(lambda value: value == other)

    def __lt__(self, other):
        return self.apply(lambda value: value < other)

    def __gt__(self, other):
        return self.apply(lambda value: value > other)

    def __le__(self, other):
        return self.apply(lambda value: value <= other)

    def __ge__(self, other):
        return self.apply(lambda value: value >= other)

    # def __neg__(self):
    #     return self.apply_unary(operator.__neg__)

    def __nonzero__(self):
        return self.apply(lambda value: not value)



import unittest

class AssertionTestCase(unittest.TestCase):
    def test_gte(self):
        x = 2
        lower = 1
        greater = 3
        equal = 2

        assertion = Assertion(x)


        print()
        print("assertion:", type(assertion), assertion)
        print()
        import ipdb
        ipdb.set_trace()
        print()
        
        
        assertion >= 1
        assertion == 2
        assertion <= 3
