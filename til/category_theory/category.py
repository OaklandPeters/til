import typing
import abc

from ..python.class_properties import classproperty, abstractclassproperty


class Category(metaclass=abc.ABCMeta):
    """
    This is structured rather differently than the Haskell version.
    """
    @abstractclassproperty
    def Morphism(cls):
        pass

    @abstractclassproperty
    def Element(cls):
        pass

