#!/usr/bin/env python

# # #
# template script
# 1) copy it under a day-related directory
# 2) fill in TODOs
#

import re
import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = 'DD'  # TODO
DEBUG = int(os.environ.get('DEBUG', 0))


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    # TODO
    return 0


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    return 0


tests = [
    # (utils.load_input('test.1.txt'), exp1, exp2),
    # TODO
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
    exp1 = -1
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = -1
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    # run_real()
