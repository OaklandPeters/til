from list_monad import List


class Tree:
    """Depends on the list monad."""
    value = None
    children = []

    def __init__(self, value=None, children=None):
        self.value = value

        if children is None:
            self.children = List.zero()
        else:
            self.children = List([elm for elm in children])

    def __repr__(self):
        return str.format(
            "{0}({1}, {2})",
            self.__class__.__name__,
            repr(self.value),
            repr(self.children)
        )


    @classmethod
    def zero(cls):
        return cls()

    def __iter__(self):
        return iter(self.children)

    def append(self, other):
        cls = type(self)
        accumulator = (List
                       .zero()
                       .append(self.children)
                       .append(List([other.value]))
                       .append(other.children)
        )
        return cls(self.value, accumulator)

    def join(self):
        cls = type(self)
        accumulator = cls.zero()
        for elm in self:
            if isinstance(elm, cls):
                accumulator = accumulator.append(elm)
            else:
                accumulator = accumulator.append(cls(elm))
        return cls(self.value, accumulator)

    def filter(self, function):
        """Applies to children"""
        cls = type(self)
        accumulator = cls.zero()
        for child in self.children:
            if function(child):
                accumulator = accumulator.append(child)
        return cls(self.value, *accumulator)

    def map(self, function):
        cls = type(self)
        return cls(
            function(self),
            List(function(elm) for elm in self.children)
        )

    @classmethod
    def _traverse(cls, elm, function):
        if isinstance(elm, cls):
            return elm.traverse(function)
        elif isinstance(elm, List):
            return elm.traverse(function)
        else:
            return function(elm)
    
    def traverse(self, function):
        return self.map(lambda elm: self._traverse(elm, function))

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        elif self.value != other.value:
            return False
        elif len(self.children) != len(other.children):
            return False
        else:
            for left, right in zip(self.children, other.children):
                # This step may recurse when left is a List
                if left != right:
                    return False
            return True
