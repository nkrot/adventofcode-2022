#!/usr/bin/env python

# # #
#
#

import os
import sys
from typing import List, Dict, Union

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '21'
DEBUG = int(os.environ.get('DEBUG', 0))


class Stree(object):

    @classmethod
    def from_text(cls, lines):
        obj = cls()
        for line in lines:
            fields = line.replace(':', '').split()
            trgvar = fields.pop(0)
            if len(fields) == 1:
                rhs = cls.Value(fields[0])
            elif len(fields) == 3:
                rhs = cls.Expression(fields[1], fields[0], fields[2], trgvar)
            obj[trgvar] = rhs
        return obj

    def __init__(self):
        self.variables: Dict[str, Union[self.Value, self.Expression]] = {}

    def __setitem__(self, varname, value: Union["Value", "Expression"]):
        self.variables[varname] = value
        value.registers = self

    def __getitem__(self, varname: str) -> Union["Value", "Expression"]:
        return self.variables[varname]

    def find(self, operand: str):
        """"""
        for lhs, rhs in self.variables.items():
            if isinstance(rhs, self.Expression) and operand in rhs.operands:
                return rhs

    # def __str__(self):
    #     return "{} = {}".format(self.)

    class Expression():

        SYMBOLS = {
            "*": "__mul__",
            "+": "__add__",
            "/": "__floordiv__",
            "-": "__sub__",
            "=": "__eq__"
        }

        def __init__(self, op, op1, op2, trgvar):
            self.operator = op
            self.operands = [op1, op2]
            self.target = trgvar
            self.registers = None

        def eval(self) -> int:
            if self.operator == "=":
                # unary operator
                op = self.operands[0]
                return getattr(self.registers[op], "eval")()
            else:
                # binary operators
                values = [
                    getattr(self.registers[op], "eval")()
                    for op in self.operands
                ]
                return getattr(values[0], self.SYMBOLS[self.operator])(values[1])

        def __str__(self):
            return "{} = ({} {} {})".format(self.target, self.operator,
                *self.operands)

        def transform(self, trgvar):
            """ Transform current expression to express term `trgvar` from it
            For example, given
                y = a + x
            extracting `a`, results in
                a = y - x
            """
            i = self.operands.index(trgvar)
            j = (i + 1) % 2
            # print("express", trgvar, "from", self, i)
            othervar = self.operands[j]
            if self.operator == "+":
                expr = self.__class__("-", self.target, othervar, trgvar)
            elif self.operator == "*":
                expr = self.__class__("/", self.target, othervar, trgvar)
            elif self.operator == "-":
                if i == 0:
                    expr = self.__class__("+", self.target, othervar, trgvar)
                else:
                    expr = self.__class__("-", othervar, self.target, trgvar)
            elif self.operator == "/":
                if i == 0:
                    expr = self.__class__("*", self.target, othervar, trgvar)
                else:
                    expr = self.__class__("/", othervar, self.target, trgvar)
            elif self.operator == "=":
                expr = self.__class__("=", othervar, 0, trgvar)
            else:
                raise NotImplementedError(
                    "Life sucks for expressing",
                    trgvar, "from", str(self), i
                )
            expr.registers = self.registers
            return expr

    class Value():

        def __init__(self, value):
            self.value = int(value)
            self.registers = None

        def eval(self):
            return self.value

        def __str__(self):
            return str(self.value)


def parse(lines: List[str]) -> str:
    """Parse a line of input into suitable data structure"""
    return Stree.from_text(lines)


def solve_p1(expr: Stree) -> int:
    """Solution to the 1st part of the challenge"""
    return expr["root"].eval()


def transform(tree, operand):
    """Extract `operand` to ba root of the tree"""
    expr = tree.find(operand)
    trn = expr.transform(operand)
    # print("Before", expr)
    # print("After ", trn)
    if expr.operator != "=":
        transform(tree, expr.target)
    tree[trn.target] = trn


def solve_p2(tree: Stree) -> int:
    """Solution to the 2nd part of the challenge"""
    tree["root"].operator = "="
    target = "humn"
    transform(tree, target)
    return tree[target].eval()


tests = [
    (utils.load_input('test.1.txt', parser=parse), 152, 301),
]


reals = [
    (utils.load_input(parser=parse), 142707821472432, 3587647562851)
]


if __name__ == '__main__':
    utils.run_tests(DAY, tests, solve_p1, solve_p2)
    utils.run_real(DAY, reals, solve_p1, solve_p2)
