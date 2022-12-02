#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Callable

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '02'
DEBUG = int(os.environ.get('DEBUG', 0))

SCORES = {
    'A': 1,
    'B': 2,
    'C': 3
}

WINS = {
    # key wins value
    'B': 'A',
    'C': 'B',
    'A': 'C',
}

LOSES = {v: k for k, v in WINS.items()}


def play(m1: str, m2: str) -> int:
    # A - Rock, B - Paper, C - Scissors
    outcome = 0  # m2 loses
    if m1 == m2:  # a draw
        outcome = 3
    elif WINS.get(m2) == m1:  # m2 wins
        outcome = 6
    return outcome + SCORES[m2]


def play_all(lines: List[str], decoder: Callable):
    games = [(ln.split()) for ln in lines]
    # decode the meaning of the 2nd argument
    games = [(m1, decoder(m1, unk)) for m1, unk in games]
    return sum(play(*g) for g in games)


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    convs = {'X': 'A', 'Y': 'B', 'Z': 'C'}
    def decode(m1, m2):
        return convs[m2]
    return play_all(lines, decode)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""

    def decode(m1, outcome):
        # what is m2 such that the outcome is <outcome>
        m2 = m1   # Y, a draw
        if outcome == 'X':  # m2 loses
            m2 = WINS[m1]
        elif outcome == 'Z':  # m2 wins
            m2 = LOSES[m1]
        return m2

    return play_all(lines, decode)


tests = [
    (utils.load_input('test.1.txt'), 15, 12),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp)
            print(f"T.{tid}.p1:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T.{tid}.p2:", res2 == exp2, exp2, res2)


def run_real():
    lines = utils.load_input()

    print(f"--- Day {DAY} p.1 ---")
    exp1 = 10816
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 11657
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
