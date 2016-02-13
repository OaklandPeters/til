"""
Stub file for a monoid typeclass/ABC.
Has no explanation and (probably) no utility functions.
Will eventually be replaced with a more full TIL file.
"""
import typing

from ..python.class_properties import abstractclassmethod

MElement = typing.TypeVar('MElement')

class Monoid(typing.Generic[MElement]):
    @abstractclassmethod
    def mzero(self):
        return NotImplemented

    @abstractmethod
    def mappend(self, other):
        return NotImplemented
