#
#   Composition function
# -----------------------
# Writing a smart composition function
# Testing composition metafunctions
import functools

# Composition primitives (~Monoid)
_compose = lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs))
_identity = lambda x: x

def compose(*callables):
    composed = _identity
    for func in reversed(callables):
        composed = functools.wraps(func)(_compose(func, composed))
    return composed

def dumb_compose(*callables):
    return reduce(_compose, callables, _identity)

def add5(a):
    return a + 5
def mult2(a):
    return a * 2
def square(a):
    return a * a

def manual(a):
    return add5(mult2(square(a)))

smart = compose(add5, mult2, square)
dumb = dumb_compose(add5, mult2, square)

A = 3
print("Manual: ", repr(manual), " --> ", manual(A))
print("Smart:  ", repr(smart), " --> ", smart(A))
print("Dumb:   ", repr(dumb), " --> ", dumb(A))

('Manual: ', '<function manual at 0x105653668>', ' --> ', 23)
('Smart:  ', '<function add5 at 0x105653848>', ' --> ', 23)
('Dumb:   ', '<function <lambda> at 0x1056539b0>', ' --> ', 23)
