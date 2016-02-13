"""
Pythonic interfaces for monoid.
"""
import typing

mappend mempty x = x
mappend x mempty = x
mappend x (mappend y z) = mappend (mappend x y) z
mconcat = foldr mappend mempty


class Category(metaclass=abc.ABCMeta):
    @

class Monoid:
    pass


This = typing.TypeVar('ThisMonoid', bound=Monoid)


class MonoidLaws(TestLawsMixin, typing.Generic[This]):
    @abstractproperty
    def Monoid(cls) -> This:
        pass

    def test_first(self, element: This.Element):

        self.Monoid.append(self.Monoid.zero(), 
