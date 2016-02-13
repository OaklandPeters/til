"""
Stub file for a monoid typeclass/ABC.
Has no explanation and (probably) no utility functions.
Will eventually be replaced with a more full TIL file.
"""
import typing
import abc

from ..python.class_properties import abstractclassmethod


__all__ = (
    'Monoid',
    'mzero',
    'mappend'
)

MElement = typing.TypeVar('MElement')
# 'This' is a placeholder, for some kind of self-class reference
#   Until Python gets F-bounded polymorphism, ...
This = typing.TypeVar('This')


class Monoid(typing.Generic[MElement]):
    @abstractclassmethod
    def mzero(self) -> This:
        return NotImplemented

    @abc.abstractmethod
    def mappend(self, other: This) -> This:
        return NotImplemented

    @classmethod
    def mconcat(cls, foldable: 'Foldable[This]'):
        """Folds a structure, using the rules of this monoid."""
        return foldable.foldr(cls.mappend, cls.mzero())


# ===========================
# Generic functions
# ===========================


def mappend(left: Monoid, right: Monoid):
    return left.mappend(right)


def mzero(monoid: Monoid):
    return monoid.mzero()

# mconcat: writing this function has problems, because
# it uses the functions on a Monoid *class*, to fold up
# a foldable *instance*
#
