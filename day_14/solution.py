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
from aoc.utils import Vector, Matrix, flatten, mdrange


DAY = '14'
DEBUG = int(os.environ.get('DEBUG', 0))


class Point(Vector):
    """for purposes of clearer naming"""

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def __lt__(self, other: 'Point'):
        return self.x < other.x or self.x == other.x and self.y < other.y

class Cave(Matrix):
    pass


def parse_line(line: str) -> List[Point]:
    """Parse a line of input into suitable data structure"""
    points = [
        Point((int(m[1]), int(m[2])))
        for m in re.finditer(r'(\d+),(\d+)', line)
    ]
    return points


def parse_lines(points: List[Vector]):
    # find the leftmost values of x and y and treats them as origin of
    # the coordinates. This will reduce the matrix size.
    sand = Point((500, 0))  # where each sand unit starts
    allpoints = flatten(points) + [sand]
    xs = [pt.x for pt in allpoints]
    ys = [pt.y for pt in allpoints]
    new_origin = Point((min(xs), min(ys)))  # top left corner

    # Shift all points w.r.t to the new origin.
    shifted_points = [[pt - new_origin for pt in pts] for pts in points]
    # and shift the point from which sand is falling
    sand = sand - new_origin
    # print("Sandquelle", sand)

    # Represent the cave as a matrix
    last = Point([max(xs), max(ys)]) - new_origin + (1,1)
    cave = Cave(*last)

    # draw the rocks:
    for pts in shifted_points:
        for start, end in zip(pts, pts[1:]):
            startx, endx = sorted([start.x, end.x])
            starty, endy = sorted([start.y, end.y])
            for x, y in mdrange((startx, endx+1), (starty, endy+1)):
                cave[x,y] = 2
    if DEBUG:
        print("== initial cave with rocks ==")
        print(cave)
    return cave, sand

MOVES = [
    (0, +1), # down
    (-1, +1), # down-left
    (+1, +1) # down-right
]


def move_sand(cave, grit) -> bool:
    """compute position of the current grid of sand where it comes
    to rest and write 1 at that position.

    Return
    True if the grit came to rest
    False it did not and is falling into abyss
    """
    came_to_rest = False
    while not came_to_rest:
        came_to_rest = True
        for step in MOVES:
            new_pos = grit + step
            state = cave.get(new_pos, -1)
            if state == -1:
                return False
            if state == 0:
                grit = new_pos
                came_to_rest = False
                break
    cave[grit] = 1
    return came_to_rest  # must be True at this point


def solve_p1(args) -> int:
    """Solution to the 1st part of the challenge"""
    cave, sand = args
    t = 0
    while move_sand(cave, sand):
        t += 1
        if DEBUG:
            print(f"== Cave after step {t} ==")
            print(cave)
    return t


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    return 0


tests = [
    (utils.load_input(
        'test.1.txt',
        line_parser=parse_line,
        parser=parse_lines
     ), 24, None),
]


reals = [
    (utils.load_input(line_parser=parse_line, parser=parse_lines),
        755, None)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
