"""
Definitional statements for the 'fmap' method of various monads.
"""


def _maybe(function, element: 'Maybe', default=None):
    """[from haskell docs]
    The maybe function takes a default value, a function, and a Maybe value. If the Maybe value is Nothing, the function returns the default value. Otherwise, it applies the function to the value inside the Just and returns the result.
    """
    if isinstance(element, Nothing):
        return default
    elif isinstance(element, Just):
        return Just(function(element.data))

def _list(function, element: 'List'):
    return List(function(value) for value in element.data)

def _stream(function, element: 'Stream'):
    return Stream(iter([function(value) for value in element.data]))

def _instance(function, element: 'Instance'):
    """The idea (used in Python's) that instances of a class can be
    handled by injecting a 'self' as a 1st argument.
    This basically applies a pure function as a method, with a bound argument.

    This is fairly similar to the concept of the 'State' monad, and hints at the
    concepts behind arrows.
    """
    return Instance(function(element.instance, element.data))


# ?
# How to write these?
# It would be instructive to do so
# 
# _either
# _state
# _reader
# _writer
# _continuation


