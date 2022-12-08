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

DAY = '08'
DEBUG = int(os.environ.get('DEBUG', 0))


def parse(line: str) -> str:
    """Parse a line of input into suitable data structure:
    """
    return list(map(int, list(line)))


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge

    Algorithm:
    For all surrounding trees, compute how much taller they are than
    the current tree of height <height>. This is done for every side
    of the current tree: <leftof>, <rightof>, <above>, <below>.
    If the height difference is zero on at least of one of the sides,
    the tree is deemed visible.
    """
    maxc, maxr = len(lines[0]), len(lines)

    # all trees along the edges are visible by default
    c_visible = maxc*2 + (maxr-2)*2

    for r, c in utils.mdrange((1, maxr-1), (1, maxc-1)):
        height = lines[r][c]

        # check visibility along horizontal axis
        row = lines[r]
        row = [max(0, h - height + 1) for h in row]  # diffs
        leftof, rightof = row[0:c], row[c+1:]

        if sum(leftof) == 0 or sum(rightof) == 0:
            c_visible += 1
            continue

        # check visibility along vertical axis
        column = [row[c] for row in lines]
        column = [max(0, h - height + 1) for h in column]
        above, below = column[0:r], column[r+1:]

        if sum(above) == 0 or sum(below) == 0:
            c_visible += 1

    return c_visible


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge

    Algorithm:
    For every tree, get trees on each of the four sides, rearranging
    the trees on a side in the order from the closest to farthest w.r.t.
    the current tree. For each tree on side compute how much taller
    the current tree as given side tree: a value of 0 means that both
    trees are of the same height, a value larger than 0 means the current
    tree is taller than the side tree.
    Now, to compute a score for side, we find how many trees there are
    *before* zero value is encountered. If there is no zero, then the score
    corresponds to the number of all trees on the side.
    """

    def score(trees):
        if 0 in trees:
            return trees.index(0) + 1
        return len(trees)

    maxc, maxr = len(lines[0]), len(lines)
    best_score = 0

    for r, c in utils.mdrange((1, maxr-1), (1, maxc-1)):
        height = lines[r][c]
        sides = []

        # along horizontal axis
        row = lines[r]
        row = [max(0, height-h) for h in row]  # diffs
        sides += [row[0:c][::-1], row[c+1:]]

        # along vertical axis
        column = [row[c] for row in lines]
        column = [max(0, height-h) for h in column]  # diffs
        sides += [column[0:r][::-1], column[r+1:]]

        local_score = utils.prod(map(score, sides))
        best_score = max(best_score, local_score)

    return best_score


tests = [
    (utils.load_input('test.1.txt', line_parser=parse), 21, 8),
]


reals = [
    (utils.load_input(line_parser=parse), 1681, 201684)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
