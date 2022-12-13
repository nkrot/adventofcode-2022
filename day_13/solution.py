#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from itertools import zip_longest
from functools import cmp_to_key
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '13'
DEBUG = int(os.environ.get('DEBUG', 0))


def parse(lines: List[str]) -> List:
    pairs = [[]]
    for line in lines:
        if not line:
            pairs.append([])
        else:
            pairs[-1].append(eval(line))
    return pairs


def compare(left, right, level=0) -> int:
    """Compare `left` and `right` and return one of:
        -1 -- left sorts before right
         0 -- left and right are equal
        +1 -- right sortes before left
    """
    if DEBUG:
        print(f"{' '*level}compare {left} vs {right}")

    cmp = None
    if isinstance(left, int) and isinstance(right, int):
        d = (left - right)
        return d if d == 0 else d // abs(d)

    elif isinstance(left, list) and isinstance(right, list):
        for lv, rv in zip_longest(left, right):
            if lv is None:
                return -1
            elif rv is None:
                return 1
            else:
                cmp = compare(lv, rv, 1+level)
                if cmp:
                    return cmp

    elif isinstance(left, int) and isinstance(right, list):
        return compare([left], right, level+1)

    elif isinstance(left, list) and isinstance(right, int):
        return compare(left, [right], level+1)

    else:
        raise ValueError(
            f"Comparing of types not supported {type(left)} vs {type(right)}"
        )
    return cmp


def solve_p1(pairs: List) -> int:
    """Solution to the 1st part of the challenge"""
    if DEBUG:
        print(pairs)
    res = 0
    for idx, pair in enumerate(pairs):
        cmp = compare(*pair)
        if cmp == -1:
            res += (1+idx)
            if DEBUG:
                print(f"ORDER is OK {cmp}\n")
        elif DEBUG:
            print(f"ORDER is wrong {cmp}\n")
    return res


def solve_p2(pairs: List) -> int:
    """Solution to the 2nd part of the challenge"""
    dividers = [[[2]], [[6]]]  # divider packets
    packets = list(dividers) + utils.flatten(pairs)
    sorted_packets = sorted(packets, key=cmp_to_key(compare))
    if DEBUG:
        for packet in sorted_packets:
            print(packet)
    # locations of divider packets
    locations = [1+sorted_packets.index(pck) for pck in dividers]
    return utils.prod(locations)


tests = [
    (utils.load_input('test.1.txt', parser=parse), 13, 140),
]


reals = [
    (utils.load_input(parser=parse), 5882, 24948)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
