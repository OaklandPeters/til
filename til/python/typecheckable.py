class TypeCheckableMeta(type):
    """Makes isinstance and issubclass overrideable."""

    def __instancecheck__(cls, instance):        
        if any('__instancecheck__' in klass.__dict__ for klass in cls.__mro__):
            return cls.__instancecheck__(cls, instance)
        else:
            return type.__instancecheck__(cls, instance)

    def __subclasscheck__(cls, subclass):
        if any('__subclasscheck__' in klass.__dict__ for klass in cls.__mro__):
            return cls.__subclasscheck__(subclass)
        else:
            return type.__subclasscheck__(cls, subclass)


class TypeCheckable(metaclass=TypeCheckableMeta):
    """
    Convenience class, mostly used for defining amorphous non-concrete types.
    Sometimes used for runtime value type checking.
    """


def type_check(value, *klasses, name='object'):
    if not any(isinstance(value, klass) for klass in klasses):
        return TypeError(str.format(
            "{0} should be type {1}, not '{2}'",
            name.capitalize(),
            ", ".join("'{0}'".format(klass) for klass in klasses),
            type(value).__name__,
        ))
    return value


def type_check_sequence(sequence, *klasses, name='object'):
    for i, value in enumerate(sequence):
        type_check(value, *klasses, name="{0}[{1}]".format(name, i))
    return sequence
