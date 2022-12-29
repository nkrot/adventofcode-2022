#!/usr/bin/env python

# # #
#
#

import os
import sys
from typing import List

import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils
from aoc.utils import Point, minmax

DAY = '18'
DEBUG = int(os.environ.get('DEBUG', 0))


def parse(lines: List[str]) -> List[Point]:
    cubes = [Point(list(map(int, ln.split(',')))) for ln in lines]
    return cubes


# how to reach surrounding cubes
OFFSETS = [
    # along x axis
    (-1, 0, 0),
    (+1, 0, 0),

    # along y axis
    (0, -1, 0),
    (0, +1, 0),

    # along z axis
    (0, 0, -1),
    (0, 0, +1),
]


def solve_p1(cubes_list: List[Point]) -> int:
    """Solution to the 1st part of the challenge"""
    # turn to dict for faster lookup
    cubes = {cube: idx for idx, cube in enumerate(cubes_list)}
    open_sides = 0
    for cube in cubes:
        for offset in OFFSETS:
            nei = cube + offset
            found = nei in cubes
            open_sides += int(not found)
    return open_sides


def solve_p2(cubes: List[Point]) -> int:
    """Solution to the 2nd part of the challenge

    Approach
    1. create a space and put all cubes in it
    2. fill the space with water starting from a point that is known to
       be outside of the cubes
    3. we count how many times water hits a cube: it happens once for
       every external side of a cube. This is the answer to the problem.
    """
    EMPTY = 0
    WATER = 1
    CUBE = 10

    # shift all by 1 to provide a space for padding on each side
    cubes = [cube + (1, 1, 1) for cube in cubes]

    # Create a 3D space that is capable of holding all the cubes.
    # The space should have 1 layer (padding) on each side
    dims = [
        2 + max([cube[d] for cube in cubes]) # add padding on each side
        for d in (0, 1, 2)
    ]
    mat = np.zeros(dims, dtype=np.int8)

    # Put all cubes in the space
    for idx, cube in enumerate(cubes):
        mat[tuple(cube)] = CUBE
    # print(mat)

    # Use BFS-like approach to fill the space with water
    # Here `points` is a queue of positions in 3D array that are being
    # explored.
    points = [Point(0, 0, 0)]  # known external point
    while points:
        pt = points.pop(0)
        idx = tuple(pt)
        if mat[idx] == EMPTY:
            mat[idx] = WATER
            # add surrounding positions to the queue
            for offset in OFFSETS:
                nei = pt + offset
                # ensure the point is inside the space and don't bother
                # adding points outside of it.
                if all(0 <= nei[d] < dims[d] for d in (0,1,2)):
                    points.append(nei)
        elif mat[idx] >= CUBE:
            # Water hits a cube side. This happens one from each open side.
            # Each time this happens, we increment the value by 1 and this
            # will tell us how many open sides (hit by water) a cube has.
            mat[idx] += 1

    # select cubes that were hit by water and compute the number of
    # individual sides that were hit.
    external_sides = sum(mat[mat > CUBE] - CUBE)

    return external_sides


tests = [
    (utils.load_input('test.1.txt', parser=parse), 64, 58),
]


reals = [
    (utils.load_input(parser=parse), 3470, 1986)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
