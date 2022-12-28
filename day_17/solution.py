#!/usr/bin/env python

# # #
# TODO:
# 1. solve_p1() runs pretty long. how to improve?

import os
import sys
from typing import List, Union, Iterable

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils
from aoc.utils import Point, Matrix, dprint
from aoc.geometry import Shape

DAY = '17'
DEBUG = int(os.environ.get('DEBUG', 0))

UP = (0, -1)
DOWN = (0, +1)
LEFT = (-1, 0)
RIGHT = (+1, 0)


class Jet(object):
    """Endless wind acting according to given jet pattern"""

    ACTIONS = {
        ">": RIGHT,
        "<": LEFT
    }

    def __init__(self, pattern: str):
        self.steps = list(pattern)
        self.pos = -1
        assert set(self.steps) == {"<", ">"}, (
            f"Wrong characters in jet pattern: {set(self.steps)}"
        )

    def push(self, obj):
        self.pos += 1
        if self.pos + 1 > len(self.steps):
            dprint(f"Jet pattern wraps at pos={self.pos}")
            self.pos = 0
        action = self.steps[self.pos]
        dprint(f"Jet #{self.pos} pushing {action}")
        return obj.move(self.ACTIONS[action])

    def __call__(self, *args):
        return self.push(*args)


class Floor(Shape):
    """A Floor is 7 units wide and its initial vertical (y) offset is 4
    to provide 3 units of space between the Rock shaped 'minus' and the floor.
    """

    def __init__(self):
        self.width = 7
        points = [Point(x, y)
                  for x, y in zip(range(self.width), [4]*self.width)]
        super().__init__(points)
        self.name = "floor"

    def adjust_spacing_to(self, rock) -> int:
        """Move the floor down such to provide exactly 3 units of space between
        the floor and the rock.
        In this task, there is no need to move the floor up, this scenario is
        not implemented
        """
        dy = 4 - (self.top().y - rock.bottom().y)
        if dy > 0:
            self.move(DOWN, dy)
        elif dy < 0:
            self.move(UP, abs(dy))
        return dy

    def height(self):
        top = self.top()
        bottom = self.bottom()
        return bottom.y - top.y + 1


class Rock(Shape):

    shapes = {
        "minus":  [(2, 0), (3, 0), (4, 0), (5, 0)],
        "plus":   [(3, 0), (2, 1), (4, 1), (3, 2), (3, 1)], # last not necessary
        "angle":  [(4, 0), (4, 1), (4, 2), (3, 2), (2, 2)],
        "vbar":   [(2, 0), (2, 1), (2, 2), (2, 3)],
        "square": [(2, 0), (3, 0), (2, 1), (3, 1)]
    }

    sequence_of_shapes = ("minus", "plus", "angle", "vbar", "square")
    sequence_pos = -1

    # TODO: make generator of new rocks into a separate class
    # that will perform Rock.reset() under the hood.

    @classmethod
    def reset(cls):
        cls.sequence_pos = -1

    @classmethod
    def next(cls) -> "Rock":
        """Create and return the Rock of predefined shape"""
        cls.sequence_pos += 1
        if cls.sequence_pos + 1 > len(cls.sequence_of_shapes):
            cls.sequence_pos = 0
        name = cls.sequence_of_shapes[cls.sequence_pos]
        points = [Point(x, y) for x, y in cls.shapes[name]]
        obj = cls(points)
        obj.name = name
        return obj

    def move(self, *args):
        self.prev_points = self.points
        super().move(*args)

    def undo(self):
        """Undo the most recent move"""
        self.points = self.prev_points

    def fall(self, times: int = 1):
        for _ in range(times):
            self.move(DOWN)
        return self


def parse(lines: List[str]) -> str:
    assert len(lines) == 1, "Wrong number of lines read"
    return Jet(lines[0])


def move_a_rock(rock, jet, floor):
    """Move the rock until it lands on the floor or another rock"""
    # print("..initial rock")
    # print(rock)
    while True:
        jet.push(rock)
        minx, maxx = rock.left().x, rock.right().x
        if minx < 0 or maxx >= floor.width or floor.overlaps_with(rock):
            dprint("..undoing side move")
            rock.undo()
        dprint("rock falling")
        rock.fall()
        if floor.overlaps_with(rock):
            dprint("..undoing fall")
            rock.undo()
            break
    # At this point, the rock landed on the floor and the rock gets merged
    # into the floor.
    floor += rock


def solve_p1(jet: Jet, num_rocks: int = 2022) -> int:
    """Solution to the 1st part of the challenge"""
    # num_rocks = 11 # debug
    Rock.reset()
    floor = Floor()
    rock = None
    for idx in range(num_rocks):
        # print(f"Rock #{1+idx}")
        rock = Rock.next()
        floor.adjust_spacing_to(rock)
        move_a_rock(rock, jet, floor)
    if DEBUG:
        print("--- DONE ---")
        print(floor)
        bottom = floor.bottom()
        canvas = Matrix(1+bottom.y, floor.width, ".")
        floor.draw(canvas)
        rock.draw(canvas)
        print(canvas)
    return floor.height() - 1 # excluding the hight of the initial floor


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    # after 1_000_000_000_000 rocks fell
    # filling of the chamber repeats. find out repetition period and
    # skip as many simulations as possible
    return 0


tests = [
    (utils.load_input('test.1.txt', parser=parse), 3068, 1514285714288),
]


reals = [
    (utils.load_input(parser=parse), 3232, None)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
