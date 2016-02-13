# Singletons & the Necessity of Metaclasses

The [singleton design pattern](https://en.wikipedia.org/wiki/Singleton_pattern) is a pattern that restricts instantiation of a class to only one object. It is often critized as being an anti-pattern, and in most cases I agree. However, it does have (rare) legitimate uses.

Designing a singleton in Python highlights some of the reasons that metaclasses are necessary - and provides an interesting lesson about the implementation of the standard `type` metaclass.

A naive attempt to write a singleton class, via the class's `__new__` method:

```python3
class MyFailedSingleton:
    def __new__(cls, *args, **kwargs):
        # Goal: create an instance the first time, cache, and always return it
        if not getattr(cls, '_singleton_cache', None):
            # Construct instance
            self = object.__new__(cls)
            # Call init code
            self.__init__(*args, **kwargs)
            setattr(cls, '_singleton_cache', self)
        # Return the cached instance...
        return cls._singleton_cache
        # BUT there is a problem:
        # Python's default metaclass (type) does something inconvenient
        #    (in this case)
        # If cls.__new__ returns an instance with type == cls
        # Then the metaclass automatically calls __init__ on it.
        # So.... we need to override that behavior at the metaclass level

    def __init__(self, data):
        print("Initializing {0} with {1}".format(self.__class__.__name__, data))
        self.data = data
```

In practice, here is what goes wrong:

```python3
failed_a = MyFailedSingleton('aa')
# 'Initializing MyFailedSingleton with aa'
# 'Initializing MyFailedSingleton with aa'
# ... init called twice because of type.__call__ automatically
assert failed_a.data == 'aa'

failed_b = MyFailedSingleton('bb')
assert failed_a.data == 'bb'
assert failed_b.data == 'bb'
```


So, the default metaclass for this class implements some behavior for the constructor (in `type.__call__`) that makes this approach fail. One interesting insight here, is that the metaclass function responsible for instance construction (`__new__`) and instantiation (`__init__`) is *not* the `type.__new__`, but rather `type.__call__`.

So, a direct fix to this problem is to override the metaclass's `__call__` behavior:

```python3
class SingletonMeta(type):
    def __call__(cls, *args, **kwargs):
        if not getattr(cls, '_singleton_cache', None):
            self = type.__call__(cls, *args, **kwargs)
            setattr(cls, '_singleton_cache', self)
        return cls._singleton_cache
        

class MyWorkingSingleton(metaclass=SingletonMeta):
    def __init__(self, data):
        print("Initializing {0} with {1}".format(self.__class__.__name__, data))
        self.data = data
```

Using this works the way we expect - you can call the constructor for our singleton class multiple times - but the initializer only is called once, and we only ever get back the first instance:

```python3
working_a = MyWorkingSingleton('aa')
assert working_a.data == 'aa'
working_b = MyWorkingSingleton('bb')
assert working_a.data == 'aa'
assert working_b.data == 'aa'
```
