#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Dict
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '16'
DEBUG = int(os.environ.get('DEBUG', 0))

# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
pat = re.compile(r'Valve ([A-Z]+) has flow rate=(\d+);.+valves?((?:,? (?:[A-Z]+))+)$')


def parse(lines: List[str]) -> str:
    rooms, valves = defaultdict(set), {}
    for line in lines:
        m = pat.search(line)
        src = m[1]
        valves[src] = int(m[2])
        trgs = m[3].replace(',', " ").split()
        rooms[src].update(trgs)
    return rooms, valves


def show(rooms, valves):
    if not DEBUG:
        return
    print("--- Rooms ---")
    for src, trgs in rooms.items():
        print(src, "->", sorted(trgs))
    print("--- Valves with Flow Rates ---")
    print(valves)


def floyd_warshall(G: Dict[str, List[str]]):
    """Find shortest paths between all pairs of vertices of graph `G`"""
    INF = 999
    # print("--- Floyd-Warshall ---")
    vertices = set(G.keys())
    vertices.update(*G.values())
    vertices = sorted(vertices)
    # print("Vertices", vertices)
    distances = {
        v: {
            u: 0 if u == v else
               1 if u in G.get(v, [])
               else INF
            for u in vertices
        }
        for v in vertices
    }
    for k in vertices:
        # paths between (u,v) going though vertex k
        for u in vertices:
            for v in vertices:
                distances[u][v] = min(distances[u][v],
                                      distances[u][k] + distances[k][v])
    # for u, vs in distances.items():
    #     print(u, ":", list(vs.values()))
    return distances


def solve_p1_rec(
    start: str,
    available_time: int,
    distances,
    valves,
    destinations: List[str] = None
):
    """Recursive solver

    TODO: stop exploring a solution if it is worse than an already found
    solution.
    """

    def evaluate(dest, available_time):
        """Compute the value of going from vertex `start` to `dest`.
        The value if proportional to how much pressure a valve can release
        during the time valve remains open.
        """
        time_to_open = distances[start][dest] + 1
        time = available_time - time_to_open
        value = time * valves[dest] if time > 0 else 0
        return (time_to_open, value)

    if available_time <= 0:
        # print("Time expired")
        return 0

    if destinations is None:
        # rooms with valves where it makes sense to go
        destinations = [v for v in valves if valves[v] > 0]
    elif not destinations:
        # print("End of sequence reached")
        return 0

    best = 0
    for idx, dest in enumerate(destinations):
        time_used, released_pressure = evaluate(dest, available_time)
        other_destinations = destinations[0:idx] + destinations[idx+1:]
        released_pressure += solve_p1_rec(
            dest, available_time - time_used,
            distances, valves, other_destinations)
        best = max(best, released_pressure)

    return best


def solve_p1(args) -> int:
    """Solution to the 1st part of the challenge"""
    rooms, valves = args
    show(rooms, valves)
    distances = floyd_warshall(rooms)
    released_pressure = solve_p1_rec("AA", 30, distances, valves)
    return released_pressure


def solve_p2(args) -> int:
    """Solution to the 2nd part of the challenge"""
    rooms, valves = args
    distances = floyd_warshall(rooms)
    released_pressure = solve_p1_rec("AA", 26, distances, valves)
    return released_pressure


tests = [
    (utils.load_input('test.1.txt', parser=parse), 1651, 1707),
]


reals = [
    # (utils.load_input(parser=parse), 1559, None)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    # utils.run_real(DAY, reals, solve_p1, solve_p2)
