class classproperty:
    """Read-only."""

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class abstractclassproperty(classproperty):
    """abstract check happens in __init__, and only for classes
    descending from metaclass=abc.ABCMeta. In those cases, if the abstract
    methods have not been concretely implemented, it will raise TypeError.
    """

    __isabstractmethod__ = True
