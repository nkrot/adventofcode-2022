#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple, Callable

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '04'
DEBUG = int(os.environ.get('DEBUG', 0))


def parse(line: str) -> List[Tuple[int, int]]:
    m = re.match(r'(\d+)-(\d+),(\d+)-(\d+)$', line)
    return [
        (int(m[1]), int(m[2])),
        (int(m[3]), int(m[4]))
    ]


def is_contained(ts) -> bool:
    ta, tb = sorted(ts)
    return ta[1] >= tb[1] or ta[0] == tb[0]


def overlap(ts) -> bool:
    ta, tb = sorted(ts)
    return ta[0] <= tb[0] <= ta[1]


def solve(lines: List[str], evaluate: Callable) -> int:
    return sum(map(evaluate, map(parse, lines)))


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    return solve(lines, is_contained)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve(lines, overlap)


tests = [
    (utils.load_input('test.1.txt'), 2, 4),
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
    exp1 = 550
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 931
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
