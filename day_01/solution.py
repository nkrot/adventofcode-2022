#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Union
from functools import reduce

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '01'
DEBUG = int(os.environ.get('DEBUG', 0))


def parse(line: str) -> Union[int, None]:
    if len(line):
        return int(line)
    return None


def sum_by_group(a: List[int], b: Union[int, None]) -> List[int]:
    if b is None:
        a.append(0)
    else:
        a[-1] += b
    return a


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    sums = reduce(sum_by_group, lines, [0])
    return max(sums)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    sums = sorted(reduce(sum_by_group, lines, [0]), reverse=True)
    return sum(sums[:3])


tests = [
    (utils.load_input('test.1.txt', line_parser=parse), 24000, 45000),
]

reals = [
    (utils.load_input(line_parser=parse), 71023, 206289)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
