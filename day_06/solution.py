#!/usr/bin/env python

# # #
#
#

import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '06'
DEBUG = int(os.environ.get('DEBUG', 0))


def parse(lines: List[str]) -> str:
    """Parse a line of input into suitable data structure"""
    return lines[0]


def solve_p1(line: str, size=4) -> int:
    """Solution to the 1st part of the challenge"""
    for end in range(size, len(line)+1):
        chars = set(line[end-size:end])
        if len(chars) == size:
            return end
    return -1


def solve_p2(line: str) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(line, 14)


def solve_p1_v2(line: str):
    chars = []
    i = 0
    while len(chars) < 4:
        if line[i] in chars:
            del chars[:chars.index(line[i])+1]
        chars.append(line[i])
        i+=1
    return i


tests = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", None, 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26),
]


reals = [
    (utils.load_input(parser=parse), 1300, 3986)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1_v2, solve_p2)
    utils.run_real(DAY, reals, solve_p1_v2, solve_p2)
