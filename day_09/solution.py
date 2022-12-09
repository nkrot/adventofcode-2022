#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '09'
DEBUG = int(os.environ.get('DEBUG', 0))

# (0,0) is top left. x is horizontal, y is vertical
OFFSETS = {
    "R": (+1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, +1)
}

def parse(line: str) -> str:
    """Parse a line of input into suitable data structure:
    """
    d, steps = line.split()
    return (OFFSETS[d], int(steps))


def move_tail_knot(head: Tuple[int, int], tail: Tuple[int, int]):
    """Compute new state of `tail` given the state of `head`
    """
    # distance between head and tail knot
    dx, dy = head[0]-tail[0], head[1]-tail[1]
    if abs(dx) in {0, 1} and abs(dy) in {0, 1}:
        # if head and tail are adjacent, do nothing
        tx, ty = 0, 0
    else:
        # move current knot, at most one step regardless of how far are
        # the knotes from each other.
        tx = dx // abs(dx) if dx else dx
        ty = dy // abs(dy) if dy else dy
    return (tail[0]+tx, tail[1]+ty)


def solve_p1(moves: List, num_of_tail_knots: int = 1) -> int:
    """Solution to the 1st part of the challenge"""
    # print("Moves", moves)
    visited = {}
    head = (0, 0)
    knots = [(0, 0) for _ in range(num_of_tail_knots)]
    visited[knots[-1]] = 1
    # print("Initial\t", head, knots)
    for (mx, my), steps in moves:
        for _ in range(steps):
            # move the head knot
            head = (head[0]+mx, head[1]+my)
            # move all tail knots one by one
            for idx, tail in enumerate(knots):
                _head = knots[idx-1] if idx else head
                knots[idx] = move_tail_knot(_head, tail)
            visited[knots[-1]] = 1
            # print(head, knots[-1])

    # print("Final\t", head, knots)
    return len(visited)


def solve_p2(moves: List) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(moves, 9)


tests = [
    # debug
    # (utils.load_input('test.2.txt', line_parser=parse), 5, None),

    # task examples
    (utils.load_input('test.1.txt', line_parser=parse), 13, 1),
    (utils.load_input('test.3.txt', line_parser=parse), None, 36),
]


reals = [
    (utils.load_input(line_parser=parse), 5695, 2434)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
