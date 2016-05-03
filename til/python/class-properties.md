# Class Properties

To create getter properties on classes (which is very common in Pythons implementation of category-theory concepts), the following can be used:

```python3

class classproperty(object):
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

```

These are read-only, due to subtle issues with the way that getters and setters interact with metaclasses in Python. 
