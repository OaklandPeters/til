"""
Goal:    write breadth-first-search and depth-first-search as differing only by 1 swapped line
"""
import types


class List:
    """
    append
    map
    join
    filter
    """
    def __init__(self, values=None):
        if values is None:
            self.values = []
        else:
            self.values = [elm for elm in values]

    def __repr__(self):
        return str.format(
            "{0}[{1}]",
            self.__class__.__name__,
            ", ".join(repr(elm) for elm in self)
        )

    @classmethod
    def zero(cls):
        return cls()

    def __iter__(self):
        return iter(self.values)

    def append(self, other):
        return type(self)([elm for array in (self, other) for elm in array])
    
    def map(self, function):
        return type(self)(function(elm) for elm in self)

    @classmethod
    def _traverse(cls, elm, function):
        if isinstance(elm, cls):
            return elm.traverse(function)
        else:
            return function(elm)
    
    def traverse(self, function):
        # return type(self)(self._traverse(elm, function) for elm in self)
        return type(self)(self.map(lambda elm: self._traverse(elm, function)))


    def filter(self, function):
        return type(self)(elm for elm in self if function(elm))

    def join(self):
        cls = type(self)
        accumulator = cls.zero()
        for elm in self:
            if isinstance(elm, cls):
                accumulator = accumulator.append(elm)
            else:
                accumulator = accumulator.append(cls([elm]))
        return accumulator

    # list magic methods
    def __len__(self):
        return len(self.values)

    def __contains__(self, value):
        return value in self.values

    def __getitem__(self, index):
        return self.values[index]

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        elif len(self) != len(other):
            return False
        else:
            for left, right in zip(self, other):
                # This step may recurse when left is a List
                if left != right:
                    return False
            return True

    def __ne__(self, other):
        return not (self == other)

    @classmethod
    def recurse(cls, function):
        def wrapper(element):
            if isinstance(element, cls):
                return wrapper(element)
            else:
                return function(element)
        return wrapper




class Node:
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
        # cls = type(self)
        # return cls(
        #     function(self.value),
        #     List(cls._traverse(elm, function) for elm in self.children)
        # )
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


#
#   Traversal functions
#
def traverse(elm, function):
    """Utility function in recursive traversals."""
    if hasattr(elm, 'traverse'):
        return elm.traverse(function)
    else:
        return function(elm)

def identity(x):
    return x

def iterator_traversal(node, function=identity):
    """~ BFS flat iterator for a tree.
    @todo: Write this with .traverse
    """    
    yield function(node.value)
    for child in node.children:
        yield from iterator_traversal(child, function)

def tree_nodes_iter(tree):
    """~ BFS flat iterator for a tree.
    @todo: Write this with .traverse
    """
    yield tree.value
    for node in tree.children:
        yield from tree_nodes_iter(node)




#
# Testing utility functions
#

def add2(x):
    return int.__add__(x, 2)

def counter(initial=0, step=1):
    counter = initial
    while(True):
        yield counter
        counter += 1
from_zero = counter(initial=0)

def inc():
    return next(from_zero)

def is_all(x):
    return (x % 1 == 0)

def is_even(x):
    return (x % 2 == 0)

def is_odd(x):
    return (x % 2 == 1)
def last_char_is_odd(word):
    return is_odd(int(word[-1]))

def last_char_is_even(word):
    return is_even(int(word[-1]))



explicit = Node('0', [
    Node('0-0', [
        Node('0-0-0', [
            Node('0-0-0-0'),
            Node('0-0-0-1'),
        ]),
        Node('0-0-1'),
        Node('0-0-2', [
            Node('0-0-2-0'),
            Node('0-0-2-1'),
            Node('0-0-2-2'),
        ])
    ]),
    Node('0-1'),
    Node('0-2', [
         Node('0-2-0')
    ]),
])
tree = Node(inc(), [
    Node(inc(), [
        Node(inc(), [
            Node(inc()),
            Node(inc()),
        ]),
        Node(inc(), []),
    ]),
    Node(inc(), []),
    Node(inc(), [
         Node(inc(), [])
    ]),
])


def _DFS(node, check):
    return (
        List([node.value])
        .filter(check)
        .append(
            node.children  # if children is Zero --> map returns zero
            .map(lambda child: _DFS(child, check))
            .filter(check)
        )
        .join()
    )


def DFS(node, check):
    return (
        List
        .zero()
        .append(
            _DFS(node, check)
        )
    )

def BFS(node, check):
    return (
        List([node.value])
        .append(
            node.children
            .map(lambda child: child.value)
        )
        .append(
            node.
        )
    )
    # return (
    #     List
    #     .zero()
    #     .append(
    #         node.children
    #         .map(lambda node: BFS(node, check))
    #     )
    #     .append(
    #         List([node.value])
    #     )
    #     .join()
    #     .filter(check)
    # )

def pre_merge(node):
    """This correctly gets the order of visitation for DFS."""
    return (
        List
        .zero()
        .append(
            node.children
            .map(pre_merge)
            .join()
        )
        .append([node.value])
        # .join()
    )

def post_merge(node):
    return _post_merge(Node('None', [node]))

def _post_merge(node):
    """This approximately gets the ordering correct of BFS, 
    but is ~joining them incorrectly.

    post = post_merge(explicit)
    post[0] == '0'
    post[1] == List['0-0', ... the descendants of 0-0, ...
    post[2] == List['0-1', ... the descendants of 0-1, ...]
    """
    return (
        List
        .zero()
        # .append([node.value])
        .append(
            node.children
            .map(lambda child: child.value)
        )
        .append(
            node.children
            .map(_post_merge)
            .join()
        )        
    )



dfs_result = DFS(explicit, lambda x: True)
bfs_result = BFS(explicit, lambda x: True)

#
#   Todo: Incorporate unit-tests for these
#
bush = tree.map(identity)

twig = Node(1, [Node(2), Node(3)])
twiggy = twig.map(identity)
ttwiggy = twig.traverse(identity)
twiggy_plus2 = twig.traverse(add2)
twig_flat = twig.join()



thing = List([1, 2, List([3, 4])])
thingy = thing.map(identity)
thing_flat = thing.join()
tthingy = thing.traverse(identity)



#d_result = DFS(tree, is_odd)
#b_result = BFS(tree, is_odd)


pre = pre_merge(explicit)
post = post_merge(explicit)

print()
#print("d_result:", type(d_result), d_result)
#print("b_result:", type(b_result), b_result)
# print("pre_result:", type(pre_result), pre_result)
# print("post_result:", type(post_result), post_result)
print("pre:", type(pre), pre)
print("post:", type(post), post)
print()
import ipdb
ipdb.set_trace()
print()


import unittest

class NodeTests(unittest.TestCase):
    def test_join(self):
        self.assertEqual(
            Node(1, List([Node(3, List([4, 5]))])),
            Node(1, List([3, 4, 5]))
        )
