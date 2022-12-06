#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = 'DD'  # TODO
DEBUG = int(os.environ.get('DEBUG', 0))


def parse(line: str) -> str:
    """Parse a line of input into suitable data structure:
    """
    # TODO: implement or delete if no transformation is needed
    return line


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    # TODO
    return 0


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    return 0


tests = [
    # (utils.load_input('test.1.txt', line_parser=parse), exp1, None),
    # TODO
]


reals = [
    # (utils.load_input(line_parser=parse), None, None)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    # utils.run_real(DAY, reals, solve_p1, solve_p2)
