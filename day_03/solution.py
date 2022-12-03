#!/usr/bin/env python

# # #
#
#

import os
import sys
from typing import List
from functools import reduce

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '03'
DEBUG = int(os.environ.get('DEBUG', 0))

alphabet = [
    * map(chr, range(ord('a'), 1+ord('z'))),
    * map(chr, range(ord('A'), 1+ord('Z')))
]

PRIORITIES = {char: 1+idx for idx, char in enumerate(alphabet)}


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    common_items = []
    for ln in lines:
        mid = len(ln)//2
        lhs, rhs = ln[0:mid], ln[mid:]
        assert len(lhs) == len(rhs)
        common_items.extend(set(lhs) & set(rhs))
    # score = sum(PRIORITIES[item] for item in common_items)
    score = sum(map(PRIORITIES.get, common_items))
    return score


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    res = 0
    grp_size = 3
    for i in range(0, len(lines), grp_size):
        common_items = reduce(
            lambda a, b: a & set(b),
            lines[i+1:i+grp_size],
            set(lines[i])
        )
        assert len(common_items) == 1
        res += PRIORITIES[common_items.pop()]
    return res


tests = [
    (utils.load_input('test.1.txt'), 157, 70),
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
    exp1 = 8105
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 2363
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
