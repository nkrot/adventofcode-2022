#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Generator

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '10'
DEBUG = int(os.environ.get('DEBUG', 0))


def parse(line: str) -> str:
    """Parse a line of input into suitable data structure:
    """
    args = line.split()
    cmd = args.pop(0)
    if cmd == "noop" and not args:
        return (1, 0)
    elif cmd in {"addx",} and len(args) == 1:
        return (2, int(args[0]))
    else:
        raise ValueError("Oops", line)


def crt(instructions: List, start: int = 0) -> Generator:
    """CRT as a generator yielding at each step a 2-tuple
      * time stamp (starting at `start` or 0 by default)
      * value of Register X during the time stamp, that is, before
        corresponding instruction was executed

     REMOVED (unnecessary):
      * value of register X after the time stamp, that is once corresponding
        instruction was executed
    """
    reg_x = 1
    t = start-1
    while instructions:
        t += 1
        res = [t, reg_x]
        inst = instructions.pop(0)
        ttl, val = inst
        ttl -= 1
        if ttl == 0:
            reg_x += val
        else:
            instructions.insert(0, (ttl, val))
        # res.append(reg_x)
        yield tuple(res)


def solve_p1(instructions: List) -> int:
    """Solution to the 1st part of the challenge"""
    checkpoints = [20, 60, 100, 140, 180, 220]
    tss = 0 # total signal strength
    for t, reg_x in crt(instructions, 1):
        if checkpoints[0] == t:
            tss += t * reg_x
            checkpoints.pop(0)
        if not checkpoints:
            break
    return tss


def solve_p2(instructions: List) -> int:
    width, height = 40, 6
    display = ["."] * (height*width)

    # compute state of the pixels on the display
    for t, x in crt(instructions):
        pos_w = t % width
        sprite = (x-1, x, x+1)
        if pos_w in sprite:
            display[t] = "#"

    # draw the display
    rows = ["".join(row) for row in utils.listfold(display, width)]
    res = "\n".join(rows)
    return res


tests = [
    # (utils.load_input('test.0.txt', line_parser=parse), -1, None),
    (
        utils.load_input('test.1.txt', line_parser=parse),
        13140,
        utils.text_from("expected.p2.test.1.txt")
    ),
]


reals = [
    (
        utils.load_input(line_parser=parse),
        15260,
        utils.text_from("expected.p2.txt")  # "PGHFGLUG"
    )
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
