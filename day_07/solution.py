#!/usr/bin/env python

# # #
#
#

import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils
from aoc.tree import Tree

DAY = '07'
DEBUG = int(os.environ.get('DEBUG', 0))


class FSObject(Tree):

    @classmethod
    def Root(cls):
        o = super().Root("/")
        o.type = "dir"
        return o

    @classmethod
    def from_ls(cls, s: str):
        parts = s.split()
        o = cls(parts[1])
        if parts[0] == "dir":
            o.type = "dir"
        else:
            o._size = int(parts[0])
        return o

    def __init__(self, name=None):
        super().__init__(name)
        self.type = "file"
        self._size = 0

    @property
    def size(self):
        if self.type == "dir":
            return sum(ch.size for ch in self) or 0
        return self._size

    def find(self, name: str):
        if name == "..":
            return self.parent
        else:
            nodes = [n for n in self.children if n.name == name]
            assert len(nodes) == 1, f"OOps, found {len(nodes)} of {name} in {self}"
            return nodes[0]

    def isdir(self):
        return self.type == "dir"

    def __str__(self):
        props = [self.type]
        if not self.isdir():
            props.append(f"size={self._size}")
        return "- {} ({})".format(self.name, ", ".join(props))

    def indented(self, indent=2, sep=" "):
        _self = sep * indent * self.level + str(self)
        lines = [_self] + [ch.indented(indent=indent, sep=sep) for ch in self]
        return "\n".join(lines)


def parse(lines: List[str]) -> FSObject:
    """Parse lines of input into a Tree that represents sile system with
    Tree nodes being nodes of type `FSObject`. Each node has an attribute
    that tells whether the node is a dir(ectory) or file.
    """
    root = FSObject.Root()
    cwd = None
    for line in lines:
        if line.startswith("$"):
            argv = line.split()[1:]
            if argv[0] == "cd":
                if argv[1] == "/":
                    cwd = root
                else:
                    cwd = cwd.find(argv[1])
        else:
            cwd.add(FSObject.from_ls(line))
    return root


def solve_p1(root: FSObject) -> int:
    """Solution to the 1st part of the challenge"""
    def select(node):
        return node.isdir() and node.size <= 100000
    return sum(node.size for node in root.dfs(select))


def solve_p2(fs: FSObject) -> int:
    """Solution to the 2nd part of the challenge"""
    hdd, needed = 70000000, 30000000
    needed = needed - (hdd - fs.size)
    def select(node):
        return node.isdir() and node.size >= needed
    dirs = [node.size for node in fs.dfs(select)]
    dirs.sort()
    return dirs[0]


tests = [
    (utils.load_input('test.1.txt', parser=parse), 94853 + 584, 24933642),
]


reals = [
    (utils.load_input(parser=parse), 1454188, 4183246)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
