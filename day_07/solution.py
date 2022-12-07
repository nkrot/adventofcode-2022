#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Callable

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '07'
DEBUG = int(os.environ.get('DEBUG', 0))


class Node(object):

    @classmethod
    def Root(cls):
        o = cls()
        o.name = "/"
        o.type = "dir"
        o._level = 0
        return o

    @classmethod
    def from_ls(cls, s: str):
        o = cls()
        parts = s.split()
        if parts[0] == "dir":
            o.type = "dir"
        else:
            o._size = int(parts[0])
        o.name = parts[1]
        return o

    def __init__(self):
        self.type = "file"
        self.name = None
        self._size = 0
        self.children = []
        self.parent = None
        self._level = None

    def add(self, node):
        node.parent = self
        # TODO: detect duplicates?
        self.children.append(node)

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

    @property
    def level(self):
        if self._level is None:
            self._level = self.parent.level + 1
        return self._level

    def __str__(self):
        if self.isdir():
            return "- {} ({})".format(self.name, self.type)
        else:
            return "- {} ({}, size={})".format(self.name, self.type, self._size)

    def __repr__(self):
        return str(self)

    def as_tree(self):
        _self = "  " * self.level + str(self)
        lines = [_self] + [ch.as_tree() for ch in self]
        return "\n".join(lines)

    def __iter__(self):
        return iter(self.children)


def dfs(start, selector: Callable = None):
    if not selector or selector and selector(start):
        yield start
    for ch in start:
        yield from dfs(ch, selector)


def parse(lines: List[str]) -> Node:
    """Parse lines of input into suitable data structure"""
    root = Node.Root()
    cwd = None
    for line in lines:
        if line.startswith("$ cd"):
            name = line.split()[-1]
            if name == "/":
                cwd = root
            else:
                cwd = cwd.find(name)
        elif line == "$ ls":
            pass
        else:
            cwd.add(Node.from_ls(line))
    return root


def solve_p1(root: Node) -> int:
    """Solution to the 1st part of the challenge"""
    def select(node):
        return node.isdir() and node.size <= 100000
    return sum(node.size for node in dfs(root, select))


def solve_p2(fs: Node) -> int:
    """Solution to the 2nd part of the challenge"""
    hdd, needed = 70000000, 30000000
    needed = needed - (hdd - fs.size)
    def select(node):
        return node.isdir() and node.size >= needed
    dirs = [node.size for node in dfs(fs, select)]
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
