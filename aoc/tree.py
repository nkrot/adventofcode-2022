"""
datastructure: Tree (directed graph)
"""

from typing import Callable


class Tree(object):

    # TODO: default sort order is by name?

    @classmethod
    def Root(cls, *args):
        args = args or ["ROOT"]
        obj = cls(*args)
        obj.is_root = True
        return obj

    def __init__(self, name=None):
        self.name = name
        self.parent = None
        self.children = []
        self.is_root = False

    def add(self, other: 'Tree'):
        """Add given tree `other` as a child node to the current tree"""
        # assert isinstance(other, type(self))
        other.parent = self
        other.is_root = False
        self.children.append(other)
        return self

    @property
    def level(self) -> int:
        return 0 if self.is_root else self.parent.level + 1

    def __iter__(self):
        return iter(self.children)

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.__dict__)

    def dfs(self, *args, **kwargs):
        yield from dfs(self, *args, *kwargs)


def dfs(start: "Tree", selector: Callable = None):
    """This is specific to implementation of the tree"""
    if not selector or selector and selector(start):
        yield start
    for ch in start:
        yield from dfs(ch, selector)
