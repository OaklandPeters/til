import functools
import operator
import unittest


class Assertion:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.value)

    @classmethod
    def lift(cls, value):
        return cls(value)

    def apply(self, operator, *others):
        result = operator(self.value, *others)
        if not result:
            raise AssertionError(operator.error_message(self.value, *others))
        return result

    def bind(self, function, *others):
        return self.lift(self.apply(function, *others))

    #
    # Logical Magic methods
    #
    def __ne__(self, other):
        return self.apply(NotEqual, other)

    def __eq__(self, other):
        return self.apply(Equal, other)

    def __lt__(self, other):
        return self.apply(Less, other)

    def __gt__(self, other):
        return self.apply(Greater, other)

    def __le__(self, other):
        return self.apply(LessEqual, other)

    def __ge__(self, other):
        return self.apply(GreaterEqual, other)

    def __neg__(self):
        return self.apply(Negate)

    def __nonzero__(self):
        return self.apply(lambda value: bool(value),
                          lambda value: "bool({0})".format(value))

    # These require fussing with the metaclass
    # def __subclasshook__(self, other):
    # def __instancecheck__(self, other):


class UnittestAssertion(Assertion, unittest.TestCase):
    def __init__(self, test_case, value):
        super(UnittestAssertion, self).__init__(value)
        self.test_case = test_case

    def apply(self, operator, *others):
        result = operator(self.test_case, self.value, *others)
        return self

    def map(self, function, *others):
        def adaptor(case, value, *others):
            return function(value, *others)
        return self.apply(adaptor, *others)

    #
    # Logical Magic methods
    #
    def __ne__(self, other):
        return self.map(self.test_case.assertNotEqual, other)
        # return self.apply(assertNotEqual, other)

    def __eq__(self, other):
        return self.map(self.test_case.assertEqual, other)
        # return self.apply(assertEqual, other)

    def __lt__(self, other):
        return self.map(self.test_case.assertLess, other)
        # return self.apply(assertLess, other)

    def __gt__(self, other):
        return self.map(self.test_case.assertGreater, other)
        # return self.apply(assertGreater, other)

    def __le__(self, other):
        return self.map(self.test_case.assertLessEqual, other)
        # return self.apply(assertLessEqual, other)

    def __ge__(self, other):
        return self.map(self.test_case.assertGreaterEqual, other)
        # return self.apply(assertGreaterEqual, other)



class CatchingUnittestAssertion(UnittestAssertion):
    """Exception catching"""
    def __init__(self, exceptions, test_case, value):
        super(CatchingUnittestAssertion, self).__init__(test_case, value)
        self.exceptions = exceptions




class Operator:
    symbol = NotImplemented
    function = NotImplemented

    def __init__(self, symbol, function):
        self.symbol = symbol
        self.function = function

    def __str__(self):
        return str(self.symbol)

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__,
                                  self.function.__name__)

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class BinaryAssertionOperator(Operator):
    def error_message(self, left, right):
        return str.format(
            "Untrue assertion: {0} {1} {2}",
            left, self.symbol, right)


class UnaryAssertionOperator(Operator):
    def error_message(self, value):
        return str.format(
            "Untrue assertion: {0} {1}",
            self.symbol, value)


# ===============
# Alternate method
#   ... maybe clearer
# ===============
# def NotEqual(left, right):
#     return left != right
# NotEqual.symbol = "!="

NotEqual = BinaryAssertionOperator("!=", operator.__ne__)
Equal = BinaryAssertionOperator("==", operator.__eq__)
Greater = BinaryAssertionOperator(">", operator.__gt__)
GreaterEqual = BinaryAssertionOperator(">=", operator.__ge__)
Less = BinaryAssertionOperator("<", operator.__lt__)
LessEqual = BinaryAssertionOperator("<=", operator.__le__)

IsInstance = BinaryAssertionOperator("isinstance-of", isinstance)
IsSubclass = BinaryAssertionOperator("issubclass-of", issubclass)

Negate = UnaryAssertionOperator("-", operator.__neg__)
Invert = UnaryAssertionOperator("~", operator.__invert__)


# Unittest assertion methods
assertEqual = Operator(
    "==", lambda case, left, right: case.assertEqual(left, right))
assertNotEqual = Operator(
    "!=", lambda case, left, right: case.assertNotEqual(left, right))
assertLess = Operator(
    "<", lambda case, left, right: case.assertLess(left, right))
assertLessEqual = Operator(
    "<=", lambda case, left, right: case.assertLessEqual(left, right))
assertGreater = Operator(
    ">", lambda case, left, right: case.assertGreater(left, right))
assertGreaterEqual = Operator(
    ">=", lambda case, left, right: case.assertGreaterEqual(left, right))
assertIn = Operator(
    "in", lambda case, left, right: case.assertIn(left, right))
assertNotIn = Operator(
    "not in", lambda case, left, right: case.assertNotIn(left, right))
assertIsInstance = Operator(
    "isinstance", lambda case, left, right: case.assertIsInstance(left, right))
assertTrue = Operator(
    "is_true", lambda case, value: case.assertTrue(value))
assertFalse = Operator(
    "is_false", lambda case, value: case.assertFalse(value))


class AssertionTestCase(unittest.TestCase):
    """
    Provides convience class for accessing UnittestAssertion from inside
    a TestCase class.
    """
    _Assertion = None
    @property
    def Assertion(self):
        if not self._Assertion:
            class BoundUnittestAssertion(UnittestAssertion):
                test_case = self
                def __init__(self, value):
                    super(BoundUnittestAssertion, self).__init__(self.test_case, value)
            self._Assertion = BoundUnittestAssertion
        return self._Assertion


class UnittestAssertionTests(AssertionTestCase):
    """
    @todo: add class for AssertionTestCase, which provides:
        assertion = self.Assertion(x)
        so this works:
            assertion <= 3
        -->
            self.assertLessEqual(x, 3)
    """
    # def test_boolean(self):
    #     x = True
    #     assertion = Assertion(x)

    def test_gte(self):
        x = 2
        lower = 1
        greater = 3
        equal = 2

        assertion = Assertion(x)
        _assertion = self.Assertion(x)


        print()
        print("assertion:", type(assertion), assertion)
        print()
        import ipdb
        ipdb.set_trace()
        print()
        

        assertion >= 1
        assertion == 2
        assertion <= 3

