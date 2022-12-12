#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Iterable, Callable

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils
from aoc.utils import Vector, Matrix, mdrange

DAY = '12'
DEBUG = int(os.environ.get('DEBUG', 0))

HEIGHTS = {
    chr(ch): elev
    for elev, ch in enumerate(range(ord("a"), ord("z")+1))
}


def parse(lines: List[str]) -> List[List[int]]:
    """Parse all lines of input into suitable data structure:
    """
    grid = []
    start, end = None, None
    for ridx, line in enumerate(lines):
        grid.append([])
        for cidx, ch in enumerate(list(line)):
            if ch == "S":
                start = Vector((ridx, cidx))
                ch = "a"
            if ch == "E":
                end = Vector((ridx, cidx))
                ch = "z"
            grid[-1].append(HEIGHTS[ch])
    return Matrix(grid), start, end


def around4(src: Vector, xspan=None, yspan=None):
    """xspan and yspan are [int, int)"""
    for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        trg = src + offset
        if xspan and not(xspan[0] <= trg[0] < xspan[1]):
            continue
        if yspan and not(yspan[0] <= trg[1] < yspan[1]):
            continue
        yield trg


def find_shortest_distance(
    grid: Matrix, start: Iterable, end: Iterable,
    can_proceed: Callable = None
) -> int:
    """
    The argument `can_proceed` is a function that tells if we can go
    from source position to target position.

    Returns -1 if `end` could not be reached from `start`

    TODO:
    it is possible to implement the method such that it is agnostic
    that `grid` is a Matrix?
    """
    max_x, max_y = grid.shape()
    distances = Matrix(max_x, max_y, -1)
    distances[start] = 0
    points = [start]
    done = False
    while points and not done:
        src = points.pop(0)
        src_elev = grid[src]
        for trg in around4(src, (0, max_x), (0, max_y)):
            if distances[trg] > -1:  # already visited
                continue
            trg_elev = grid[trg]
            trg_dist = distances[src] + 1
            if can_proceed is None or can_proceed(src_elev, trg_elev, trg_dist):
                points.append(trg)
                distances[trg] = trg_dist
            if trg == end:
                done = True
                break
    return distances[end]


def solve_p1(args) -> int:
    """Solution to the 1st part of the challenge"""
    def can_proceed(src, trg, *args):
        return trg - src < 2
    return find_shortest_distance(*args, can_proceed)


def solve_p2(args) -> int:
    """Solution to the 2nd part of the challenge"""
    grid, _, end = args
    lowest = HEIGHTS["a"]

    def can_proceed(src, trg, *args):
        # This is the case when two paths overlap (one contains another)
        # and we are exploring the longer path and we have passed the end
        # of the shorter path. There is no need to continue checking
        # the longer path.
        if src == lowest:
            return False
        return src - trg < 2

    max_x, max_y = grid.shape()
    min_dist = (max_x + max_y) * max_x  # worst case :)
    for x, y in mdrange((0, max_x), (0, max_y)):
        if grid[x,y] == lowest:
            dist = find_shortest_distance(
                grid, end, Vector([x,y]),
                # here we check if distance reached while exploring current
                # path is shorter than the min distance found so far.
                # If this is not the case, we dont need to explore this
                # path further. This additional pruning reduces the overall
                # distance walked by 1_783_219 - 1_505_690 = 277_529 steps.
                lambda src, trg, trg_dist: (
                    trg_dist < min_dist and can_proceed(src, trg)
                ))
            if dist > 0:
                min_dist = min(dist, min_dist)
    return min_dist


tests = [
    (utils.load_input('test.1.txt', parser=parse), 31, 29),
]


reals = [
    (utils.load_input(parser=parse), 330, 321)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
