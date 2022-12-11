#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Callable, Dict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '11'
DEBUG = int(os.environ.get('DEBUG', 0))

OPERATORS = {
    "+": "__add__",
    "*": "__mul__"
}

class Monkey(object):
    # troop = []  # all monkeys

    def __init__(self, _id):
        self.id: str = _id
        self.items: List[int] = []
        self.operation: Callable = lambda x: x
        self.test: int = None
        self.whom: Dict[bool, int] = {}
        self.count: int = 0
        self.human_operation: Callable = lambda x: x // 3

    def parse_operation(self, arg1, op, arg2):
        # old * 5, old + old
        args = [
            (lambda x: x) if arg == "old" else lambda _: int(arg)
            for arg in [arg1, arg2]
        ]
        op = OPERATORS[op]
        self.operation = lambda x: getattr(args[0](x), op)(args[1](x))

    def add(self, item):
        self.items.append(int(item))

    def play(self, others: List["Monkey"]):
        while self.items:
            self.count += 1
            current_item = self.items.pop(0)
            worry_level = self.operation(current_item)
            worry_level = self.human_operation(worry_level)
            test = not(worry_level % self.test)
            # throw initial worry level or new one?
            others[self.whom[test]].add(worry_level)

    def __str__(self):
        return "Monkey {}: (times= {} )\t{}".format(
            self.id, self.count, ", ".join(map(str, self.items)))

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.__dict__)


def parse(lines: List[str]) -> List[Monkey]:
    """Parse a line of input into suitable data structure:
    """
    monkeys = []
    monkey = None
    for line in lines:
        line = line.strip()
        # Zen of Python: make simple things as complex as possible
        #tokens = line.translate(str.maketrans(",:", "  ")).split()
        tokens = line.replace(",", "").replace(":", "").split()
        if not tokens:
            continue
        if tokens[0] == "Monkey":
            monkeys.append(Monkey(tokens[1]))
            monkey = monkeys[-1]
        elif tokens[0] == "Starting":
            monkey.items = list(map(int, tokens[2:]))
        elif tokens[0] == "Operation":
            monkey.parse_operation(*tokens[3:])
        elif tokens[0] == "Test":
            monkey.test = int(tokens[-1])
        elif tokens[1] == "true":
            monkey.whom[True] = int(tokens[-1])
        elif tokens[1] == "false":
            monkey.whom[False] = int(tokens[-1])

    if DEBUG:
        for m in monkeys:
            print(repr(m))

    return monkeys


def show(monkeys, msg = None):
    if msg is not None:
        print(msg)
    for mky in monkeys:
        print(mky)


def solve_p1(monkeys: List[Monkey], num_rounds: int = 20) -> int:
    """Solution to the 1st part of the challenge"""
    if DEBUG:
        show(monkeys, "initial")
    for r in range(num_rounds):
        for mky in monkeys:
            mky.play(monkeys)
        if DEBUG:
            show(monkeys, f"After round {1+r}")
    busiest_monkeys = sorted([mky.count for mky in monkeys])[-2:]
    monkey_business = utils.prod(busiest_monkeys)
    return monkey_business


def solve_p2(monkeys: List[Monkey]) -> int:
    """Solution to the 2nd part of the challenge"""
    return 0
    #solve_p1(monkeys, 1)
    DEBUG = 1
    num_rounds = 20

    if DEBUG:
        show(monkeys, "initial")
    for r in range(num_rounds):
        for mky in monkeys:
            mky.play(monkeys)
        if DEBUG:
            show(monkeys, f"== After round {1+r} ==")
    return 0


tests = [
    (utils.load_input('test.1.txt', parser=parse), 10605, 2713310158),
]


reals = [
    (utils.load_input(parser=parse), 118674, None)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
