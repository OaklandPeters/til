
Categories are hard to statically type in most systems, because of cyclic dependencies in the structure of `Spaces` and `Categories`. Each `Category` needs to have exactly one defined `Element` class and one defined `Morphism` class, and each subclass of the `Element` and `Morphism` interfaces should have one defined `Category` that they belong to.

Here is a specific example. Note that this do:


```python3
from abc import ABCMeta

# classproperty & abstractclassproperty defined in til/python
from ..python.class_properties import classproperty, abstractclassproperty

class Category(metaclass=abc.ABCMeta):
    """
    Note - the type-signatures of call, apply, compose, or identity are 
    valid in Python, but they *do* represent the correct logic in category-theory.

    These function-signatures would be valid if Python had proper structural
    typing rules, and/or higher-kinded types.
    """
    @abstractclassproperty
    def Element(cls):
        return NotImplemented

    @abstractclassproperty
    def Morphism(cls):
        return NotImplemented

    @abstractclassmethod
    def call(cls, morphism: 'cls.Morphism', element: 'cls.Element') -> 'cls.Element':
        return NotImplemented

    @abstractclassmethod
    def apply(cls, element: 'cls.Element', morphism: 'cls.Morphism') -> 'cls.Element':
        return NotImplemented

    @abstractclassmethod
    def compose(cls, left: 'cls.Morphism', right: 'cls.Morphism') -> 'cls.Morphism':
        return NotImplemented

    @abstractclassproperty
    def identity(cls) -> 'cls.Morphism':
        return NotImplemented


class Element(metaclass=abc.ABCMeta):
    @abstractclassproperty
    def Category(cls):
        return NotImplemented



class Morphism(metaclass=abc.ABCMeta):
    @abstractclassproperty
    def Category(cls):
        return NotImplemented


#
# Concrete Implementation
#
class ListCategory(Category):
    @classproperty
    def Element(cls) -> 'ListElement':
        return ListElement

    @classproperty
    def Morphism(cls) -> 'ListMorphism':
        return ListMorphism

    @classmethod
    def call(cls, function: 'ListMorphsim', element: 'ListElement') -> 'ListElement':
        # ...

    @classmethod
    def apply(cls, element: 'ListElement', function: 'ListMorphism') -> 'ListElement':
        # ...

    @classmethod
    def compose(cls, left: 'ListMorphism') -> 'ListMorphism':
        # ...

    @classproperty
    def identity(cls) -> 'ListMorphism':
        # ...


class ListElement:
    Category = ListCategory

    def apply(self, function: 'ListMorphism') -> 'ListElement':
        return self.Category.apply(function)


class ListMorphism:
    Category = ListCategory

    def call(self, element: 'ListElement') -> 'ListElement':
        return self.Category.call(element)

    def compose(self, other: 'ListMorphism') -> 'ListMorphism':
        return self.Category.compose(other)

    @classproperty
    def identity(cls) -> 'ListMorphism':
        return self.Category.identity
```
