#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple, Iterable, Union

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils
from aoc.utils import Vector

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
    return (Vector(OFFSETS[d]), int(steps))


def compute_move(head: Vector, tail: Vector) -> Tuple[int, int]:
    """The `head` knot is just the knot immediately preceding
    the `tail` knot
    """
    dist = head - tail
    if max(abs(dist)) < 2:  # chebyshev distance
        # if head and tail are adjacent, no moving necessary
        move = (0, 0)
    else:
        # a move is at most *one* step regardless of how far are the knotes
        # from each other.
        move = [d // abs(d) if d else d for d in dist]
    return move


def move_the_rope(knots: List[Vector], head_move: Tuple[int, int]):
    for idx, knot in enumerate(knots):
        if idx == 0:
            move = head_move
        else:
            move = compute_move(knots[idx-1], knot)
        if all(m == 0 for m in move):
            # if the current knot does not move, subsequent knots will
            # not move either. We therefore finish this time step.
            break
        knots[idx] = knot + move


def solve_p1(moves: List, rope_length: int = 2) -> int:
    """Solution to the 1st part of the challenge"""
    knots = [Vector((0, 0)) for _ in range(rope_length)]
    visited = {str(knots[-1]): 1}
    for move, times in moves:
        for _ in range(times):
            move_the_rope(knots, move)
            visited[str(knots[-1])] = 1
    return len(visited)


def solve_p2(moves: List) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(moves, 10)


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
