import functools
def exc_identity(exc, *args, **kwargs):
    return repr(exc)

def maybe_raise(_catch, _raise, messenger=exc_identity):
    """Decorator with arguments.

    @type: _catch: Union[Type[Exception], Tuple[Type[Exception]]]
    @type: _raise: Type[Exception]
    @type: messenger: Callable[[Exception, *args, **kwargs], str]

    Example:
        @maybe_raise(ValueError, ValidationError)
        def validate_input(input_value):
            # ....
            if is_invalid(input_value):
                raise ValueError
    """
    if not callable(messager):
        messager = lambda exc, *_args, **_kwargs: messager
    def outer(function):
        @functools.wraps(function)
        def inner(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except _catch as exc:
                raise _raise(messenger(exc, *args, **kwargs))
        return inner
    return outer

def maybe_404(_catch, message=exc_identity):
    return maybe_raise(_catch, Http404, exc_identity)
