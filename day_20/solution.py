#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List
from collections import deque

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '20'
DEBUG = int(os.environ.get('DEBUG', 0))


class N(object):
    def __init__(self, value, pos):
        self.value = int(value)
        self.position = pos
        self.next = None

    def __repr__(self):
        nxt = None
        if self.next:
            nxt = "({}, #{})".format(self.next.value, self.next.position)
        return "<{}: ({}, #{}) -> {}>".format(self.__class__.__name__,
            self.value, self.position, nxt)

    def __str__(self):
        return "({}, #{})".format(self.value, self.position)


def parse(lines: List[str]) -> str:
    """Parse a line of input into suitable data structure:"""
    numbers = [N(ln, idx) for idx, ln in enumerate(lines)]
    return deque(numbers)


def link(numbers: List[N]):
    """Link every element to its following element.

    Ideally, this should be done inside parse(). However, it causes
        RecursionError: maximum recursion depth exceeded
    that comes from utils.run_real() deepcopy(). TODO: fix
    """
    for i in range(1, len(numbers)):
        numbers[i-1].next = numbers[i]


def show(numbers, title=None):
    if title:
        print(title)
    print(", ".join([str(n.value) for n in numbers]))
    print(" ".join([str(n) for n in numbers]))


def mix(numbers):
    """Mix the list once, starting from the first element."""
    # show(numbers, f"--- Initial {len(numbers)} ---")
    for i in range(len(numbers)):
        n = numbers.popleft()
        # print(f"\nStep {i}, current", repr(n))
        numbers.rotate(-1*n.value)
        numbers.appendleft(n)
        # show(numbers, f"length {len(numbers)}")

        # bring next number to the beginning of the list
        n = n.next
        if n:
            pos = index(numbers, n)
            # print(pos, n)
            numbers.rotate(-1*pos)


def index(numbers, target):
    for idx, n in enumerate(numbers):
        if n == target or n.value == target:
            return idx


def compute_groove_coordinates(numbers: List[N]) -> int:
    # bring zero to the beginning of the list
    numbers.rotate(-1 * index(numbers, 0))
    # show(numbers, f"--- final {len(numbers)} ---")
    res = 0
    # find 1000th, 2000th and 3000th elements
    for _ in range(3):
        numbers.rotate(-1 * 1000)
        res += numbers[0].value
    return res


def solve_p1(numbers: List[N]) -> int:
    """Solution to the 1st part of the challenge"""
    link(numbers)
    mix(numbers)

    return compute_groove_coordinates(numbers)


def solve_p2(numbers: List[N]) -> int:
    """Solution to the 2nd part of the challenge"""

    for i in range(len(numbers)):
        numbers[i].value *= 811589153
    link(numbers)

    first = numbers[0]
    for _ in range(10):
        # Ensure that originally first element is always at the beginning
        # of the list. This is what mix() expects.
        numbers.rotate(-1 * index(numbers, first))
        mix(numbers)

    return compute_groove_coordinates(numbers)


tests = [
    (utils.load_input('test.1.txt', parser=parse), 3, 1623178306),
]


reals = [
    (utils.load_input(parser=parse), 11123, 4248669215955)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
