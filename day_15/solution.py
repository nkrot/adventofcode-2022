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
from aoc.utils import Point

DAY = '15'
DEBUG = int(os.environ.get('DEBUG', 0))


def parse(line: str) -> str:
    sensor, beacon = [
        Point(int(m[1]), int(m[2]))
        for m in re.finditer(r'x=(-?\d+), y=(-?\d+)', line)
    ]
    return (sensor, beacon)


# Example test.1.txt
#       0    5    0    5    0    5
# 9 ...#########################...
#10 ..####B######################..
#     2101-3456789012345678901234
#                 1         2
# All positions: 2 + 1 + 24 = 27
# Occupied by beacon: 1
# Therefore: 27 - 1 = 26


def solve_p1(args) -> int:
    """Solution to the 1st part of the challenge"""
    sensors_and_beacons, target_y = args
    # For both of the below we store only x coordinate, because y is known
    # and it is equal to `target_y`.
    occupied_positions = set()  # where a sensor or a beacon is located
    reached_positions = set()   # reached by the sensores
    for s, b in sensors_and_beacons:
        if s.y == target_y:
            occupied_positions.add(s.x)
        if b.y == target_y:
            occupied_positions.add(b.x)
        # Determine if the sensor can reach the line `target_y`:
        # for this, compute the distance along y axis
        reach = s.l1_dist(b)
        dist_to_y = s.l1_dist((s.x, target_y))
        # is the reach of sensor larger than the distance to target_y?
        overlap = reach - dist_to_y
        if overlap >= 0:
            # The sensor can cover one or more positions on target_y line.
            # Compute all x's coverted by the sensor
            reaches = set()
            for x in range(overlap+1):
                reaches.update({s.x+x, s.x-x})
            # print("..reaches", sorted(reaches))
            reached_positions.update(reaches)
    # From reachable positions, exclude positions already occupied by
    # the sensors and beacons.
    reached_positions.difference_update(occupied_positions)
    # print("All reached:", sorted(reached_positions))
    return len(reached_positions)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    return 0


tests = [
    ((utils.load_input('test.1.txt', line_parser=parse), 10), 26, None),
]


reals = [
    ((utils.load_input(line_parser=parse), 2000000), 4502208, None)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
