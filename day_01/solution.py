#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List
from functools import reduce

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '01'
DEBUG = int(os.environ.get('DEBUG', 0))


def grouper(a, b):
    if b:
        a[-1].append(int(b))
    else:
        a.append([])
    return a


def sum_by_group(a, b):
    if b:
        a[-1] += int(b)
    else:
        a.append(0)
    return a


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    # groups = reduce(grouper, lines, [[]])
    # print(groups)
    sums = reduce(sum_by_group, lines, [0])
    # print(sums)
    return max(sums)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    sums = sorted(reduce(sum_by_group, lines, [0]), reverse=True)
    return sum(sums[:3])


tests = [
    (utils.load_input('test.1.txt'), 24000, 45000),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp)
            print(f"T.{tid}.p1:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T.{tid}.p2:", res2 == exp2, exp2, res2)


def run_real():
    lines = utils.load_input()

    print(f"--- Day {DAY} p.1 ---")
    exp1 = 71023
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 206289
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
