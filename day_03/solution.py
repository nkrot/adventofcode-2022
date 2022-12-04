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


def solve_p2_v1(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    res = 0
    grp_size = 3
    for i in range(0, len(lines), grp_size):
        common_items = reduce(
            lambda a, b: set(a) & set(b),
            lines[i:i+grp_size]
        )
        assert len(common_items) == 1
        res += PRIORITIES[common_items.pop()]
    return res


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    res = 0
    grp_size = 3
    for i in range(0, len(lines), grp_size):
        rucksacks = map(set, lines[i:i+grp_size])
        common_items = set.intersection(*rucksacks)
        assert len(common_items) == 1
        res += PRIORITIES[common_items.pop()]
    return res


tests = [
    (utils.load_input('test.1.txt'), 157, 70),
]

reals = [
    (utils.load_input(), 8105, 2363)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
