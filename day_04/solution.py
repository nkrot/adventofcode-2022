#!/usr/bin/env python

# # #
#
#

import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '04'
DEBUG = int(os.environ.get('DEBUG', 0))


def parse(line: str) -> List[List[int]]:
    """Parse a line of input into suitable data stricture:
    [[start, end], [start, end]]
    """
    ints = list(map(int, line.replace(',', '-').split('-')))
    return [ints[:2], ints[2:]]


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    def is_contained(ts) -> bool:
        ta, tb = sorted(ts)
        return ta[1] >= tb[1] or ta[0] == tb[0]
    return sum(map(is_contained, lines))


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    def overlap(ts) -> bool:
        ta, tb = sorted(ts)
        return ta[0] <= tb[0] <= ta[1]
    return sum(map(overlap, lines))


tests = [
    (utils.load_input('test.1.txt', line_parser=parse), 2, 4),
]

reals = [
    (utils.load_input(line_parser=parse), 550, 931)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
