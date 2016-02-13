"""
Testing an implementation of Foldable for Python

I *think* fold/foldMap is useful for Foldables which are also Monoids, whereas
`foldr` does not make that assumption.


New files to write:
* Write on the pre-existing, idiomatic version of these things. Foldable --> Iterable. null -> is empty ~bool, length -> __len__, 
    elem -> __contains__
* specialized folds: concat, concatMap, and, or, any, all, minimumBy, notElem, find
"""
import abc
import typing

from ..python.class_properties import abstractclassmethod

__all__ = (
    # Interfaces / Type-Classes
    'Foldable',
    'FoldableMonoid',
    # Generic method
    'foldr',
    # Utility methods
    # Concrete Implementations
    'FoldableList',
)

Element = typing.TypeVar('Element')
OutType = typing.TypeVar('OutType')
FoldingFunction = typing.Callable[Element, [OutType]]


class Foldable(typing.Generic[Element], metaclass=abc.ABCMeta):
    """
    In Haskell, type-classes often allow you options in defining the minimal
    required functions. This is not true in Python, so I am choosing to define
    it in terms of foldr.
    I'm intentionally leaving off 'foldl' for reasons of brevity, because it deals with the
    concept of a reversable structure.

    Trivial Observation: Self = Foldable[Element]
    """
    @abc.abstractmethod
    def foldr(self,
              function: FoldingFunction,
              initial: Element,
              ) -> Element:
        """
        In implementation, this will usually need to
        dispatch over at least two cases: (1) terminal/empty,
        (2) and standard/node.
        foldr is often implemented via recursion. In Python
        this will be extremely inefficient.
        """
        return NotImplemented

    def toList(self) -> typing.List[Element]:
        """
        This is revelatory of a more general idea - that you can convert a Foldable to a Monoid.
        """
        return self.foldr(list.append, [])

    def null(self) -> bool:
        """Tests if the structure is empty."""
        return self.foldr(lambda elm: False, True)

    def length(self) -> int:
        """Determines the size of a finite structure
        by counting it. Note - in Python, if foldr is
        implemented this will be
        extremely inefficient."""
        return self.foldr(lambda count: count+1, 0)

    def elem(self, element: Element) -> bool:
        """Asks if element occurs in the structure."""
        return is_any(self, lambda left, right: left == right)





Elm = typing.TypeVar('Elm')
class MonoidicFoldable(Foldable[Elm], Monoid[Elm]):
    """This needs to inherit from Monoid, which will
    give it the methods 'mappend' and 'mempty'
    """
    def foldMap(self, function: MonoidConsructor) -> MonoidicFoldable:
        return self.foldr(function, initial=self.mempty())

    # def foldMap()
    
    # def fold()






# ===========================
#  Utility  functions
#    and specialized
#        folds
# ===========================


def foldr(structure: Foldable[Element],
          function: FoldingFunction,
          initial: OutType
          ) -> OutType:
    """Generic function version of 'foldr'."""
    return structure.foldr(function, initial)


# ===========================
#   Concrete Implementations
# ===========================



class FoldableList(list, Foldable):
    def foldr(self,
              function: typing.Callable[FoldableList, [OutType]],
              initial: FoldableList) -> :
        accumulator = initial
        for elm in self:
            function(elm, accumulator)
