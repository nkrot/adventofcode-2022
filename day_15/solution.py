#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils
from aoc.utils import Point, flatten
from aoc.geometry import BrokenLine


DAY = '15'
DEBUG = int(os.environ.get('DEBUG', 0))


class Sensor(Point):

    def __init__(self, *args):
        super().__init__(*args)
        self.reach: int = None  # reach/range of the sensor

    def __repr__(self):
        return "<{}: xy={}, reach={}>".format(
            self.__class__.__name__, tuple(self.values), self.reach)


def parse(line: str) -> str:
    sensor, beacon = [
        Point(int(m[1]), int(m[2]))
        for m in re.finditer(r'x=(-?\d+), y=(-?\d+)', line)
    ]
    sensor = Sensor(*sensor)
    sensor.reach = sensor.l1_dist(beacon)
    return (sensor, beacon)


def dprint(*msgs, **kwargs):
    if DEBUG:
        print(*msgs, **kwargs)


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
    sensors_and_beacons, target_y, _ = args
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
        # for this, compute the distance from the sensor to `target_y`
        # along y axis and compare sensor reach against this value
        dist_to_y = s.l1_dist((s.x, target_y))
        # is the reach of sensor larger than the distance to target_y?
        overlap = s.reach - dist_to_y
        if overlap >= 0:
            # The sensor can cover one or more positions on target_y line.
            # Compute all x's coverted by the sensor
            reaches = set()
            for x in range(overlap+1):
                reaches.update([s.x+x, s.x-x])
            reached_positions.update(reaches)
    # From reachable positions, exclude positions already occupied by
    # the sensors and beacons.
    reached_positions.difference_update(occupied_positions)
    # print("All reached:", sorted(reached_positions))
    return len(reached_positions)


# Part 2:
# Iterate over sensors and mark all points they can reach.
# Plus mark all points where sensors and beacons are located.
# A point that remains unmarked, is the distress beacon.
#
# Optimizations
# 1) remove past rows that are beyond the maximum reach of the sensors.
#    Iff they are not solutions. This reduces active number or rows
#    from 4.000.000 to 1.629.573
# 2) ignore x, y that are outside the working range [0, max_size].
# 3) stop when first distress beacon was found.

def solve_p2(args) -> int:
    """Solution to the 2nd part of the challenge"""
    BrokenLine.DEBUG = DEBUG

    sensors_and_beacons, _, max_size = args

    # Beacons only, as sensors will be handled in a different way.
    occupied_positions = defaultdict(set) # {y: Set[x]}
    # index sensors by y coordinate, for faster access
    sensors = defaultdict(list)  # {y: List[Sensor]}
    max_reach = 0
    for s, b in sensors_and_beacons:
        if 0 <= b.x <= max_size:
            # Keep beacons that are within working range [0, max_size]
            occupied_positions[b.y].add(b.x)
        sensors[s.y].append(s)
        max_reach = max(max_reach, s.reach)

    # dshow(sensors, occupied_positions)

    dprint("-- Searching distress beacon --")
    dprint("Max reach =", max_reach)
    rows = {}
    # both x and y coordinates are in range [0, max_size]
    for y in range(0, max_size+1):
        # Remove rows at lower y if they are out of scanners' max reach.
        # This saves memory.
        out_of_reach = y - max_reach
        if out_of_reach >= 0:
            if len(rows[out_of_reach]) > 0:
                break  # solution found
            else:
                del rows[out_of_reach]
        # Analyse current row
        rows.setdefault(y, BrokenLine(0, max_size))
        dprint(f"Looking at row y={y}: {repr(rows[y])}", flush=True)
        # mark positions occupied by beacons
        for x in occupied_positions.get(y, []):
            rows[y] -= x
        # if there is a sensor in the row, mark all points reachable by
        # the sensor(s).
        for s in sensors.get(y, []):
            mark_reachable_positions(rows, s, max_size)
        dprint(f"MARKED: y={y}: {repr(rows[y])}")
    show_rows(rows)

    # Find the row(s) that remains non empty, find the distress beacon in
    # it and compute beacon Tuning Frequency. Ideally, there must be only
    # one distress beacon but we allow multiple ones to find our bugs.
    # distress_beacons = []  # there must be only one
    tuning_freq = 0
    for y, row in rows.items():
        if len(row) > 0:
            dprint(f"non empty y={y}: {repr(row)}")
            for x in row.positions():
                tuning_freq += 4000000 * x + y
    return tuning_freq


def mark_reachable_positions(rows, sensor, max_size):
    o = sensor.y
    dprint(f"y={o}: {repr(sensor)}")
    top_y = max(o - sensor.reach, 0)
    bottom_y = min(o + sensor.reach, max_size)
    for y in range(top_y, bottom_y+1):
        rows.setdefault(y, BrokenLine(0, max_size))
        dprint(f"..marking y={y}: {rows[y]}")
        # the shape of the area covered by the sensor is a rombus:
        # the reach along X axis at y where the sensor is located is maximal
        # and reduces at any other y :
        # - at y-1 and y+1, the reach is 1 position shorter (at both sides)
        # - at y-2 and y+2, the reach is 2 positions shorter
        # r is reach at given y-offset from the position of the center.
        r = sensor.reach - abs(y-o)
        rows[y] -= (sensor.x - r, sensor.x + r)
        dprint(f"..marked y={y}: {rows[y]}")


def show_rows(rows):
    dprint("--- Rows (along y axis)---")
    for y in sorted(rows.keys()):
        dprint(f"y={y}: {repr(rows[y])}")


def dshow(sensors, positions):
    if not DEBUG:
        return
    print("--- Occupied Positions (excl. negative) ---")
    for y in sorted(positions.keys()):
        xs = sorted(positions[y])
        print(f"y: {y}, xs: {xs}")
    print("--- Sensors ---")
    for y in sorted(sensors.keys()):
        for s in sensors[y]:
            print(f"y: {y}, {repr(s)}")


tests = [
    ((utils.load_input('test.1.txt', line_parser=parse), 10, 20), 26, 56000011),
]


reals = [
    # for part 2: >= 0 and no larger than 4000000
    ((utils.load_input(line_parser=parse), 2000000, 4000000), 4502208, 13784551204480)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
