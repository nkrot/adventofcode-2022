#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple, Dict
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '05'
DEBUG = int(os.environ.get('DEBUG', 0))


def parse(lines: List[str]) -> Tuple[Dict, List]:
    """Parse the whole task into suitable data structure:"""
    stacks, moves = defaultdict(list), []
    for line in lines:
        if '[' in line:
            for idx, pos in enumerate(range(0, len(line), 4), start=1):
                crate = line[pos:pos+4]
                m = re.search(r'\[(\w+)\]', crate)
                if m:
                    stacks[idx].insert(0, m[1])
        if line.startswith("move"):
            moves.append(tuple(map(int, line.split()[1:6:2])))
    return (stacks, moves)


def solve_p1(args) -> str:
    """Solution to the 1st part of the challenge"""
    stacks, moves = args
    for (qnt, src, trg) in moves:
        # move one crate at a time
        for _ in range(qnt):
            stacks[trg].append(stacks[src].pop())
    # gather the crates that are on the top
    res = "".join([stacks[idx][-1] for idx in sorted(stacks.keys())])
    return res


def solve_p2(args) -> str:
    """Solution to the 2nd part of the challenge"""
    stacks, moves = args
    for (qnt, src, trg) in moves:
        # move all <qnt> crates ate a time
        stacks[trg].extend(stacks[src][-qnt:])
        stacks[src] = stacks[src][:-qnt]
    # gather the crates that are on the top
    res = "".join([stacks[idx][-1] for idx in sorted(stacks.keys())])
    return res


tests = [
    (utils.load_input('test.1.txt', parser=parse), "CMZ", "MCD"),
]


reals = [
    (utils.load_input(parser=parse), "TPGVQPFDH", "DMRDFRHHH")
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
