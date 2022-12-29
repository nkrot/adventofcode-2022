
import os
import itertools
import functools
from copy import deepcopy
from typing import List, Union, Tuple, Optional, Callable, Iterable, Any

DEBUG = int(os.environ.get('DEBUG', 0))


def load_input(fname: Optional[str] = None, **kwargs) -> List[str]:
    """Load file, either given or default 'input.txt' and return its content
    as a list of lines. All lines are returned, including empty ones."""
    fname = fname or 'input.txt'
    lines = []
    with open(fname) as fd:
        for line in fd:
            lines.append(line.rstrip('\r\n'))
    parse_line = kwargs.get("line_parser")
    if parse_line:
        lines = list(map(parse_line, lines))
    parse = kwargs.get("parser")
    if parse:
        lines = parse(lines)
    return lines


def text_from(fpath: str):
    with open(fpath) as fd:
        return fd.read().strip("\n")


def group_lines(data: Union[str, List[str]]) -> List[List[str]]:
    """Make groups of lines: a group is a sequence of lines that are separated
    by an empty line from another group.
    Input <data> is either of these:
    1) (str) a string that is the whole content of a file;
    2) (List[str]) a list of lines that 1) already split into individual lines.
    """
    groups = [[]]
    if isinstance(data, str):
        data = [ln.strip() for ln in data.split('\n')]
    for ln in data:
        if ln:
            groups[-1].append(ln)
        else:
            groups.append([])
    return groups


def to_numbers(lines: List[str]) -> List[int]:
    """Convert list of lines (strings) to list of ints"""
    return [int(line) for line in lines]


def dprint(*args):
    if DEBUG:
        print(*args)

def minmax(numbers: List[int]) -> Tuple[int, int]:
    """Return min and max values from given list of integers"""
    return (min(numbers), max(numbers))


def flatten(items: List[List]) -> List:
    """Flatten one level"""
    return [item for subitems in items for item in subitems]

# Source
# https://stackoverflow.com/questions/55774054/precise-time-in-nano-seconds-for-python-3-6-and-earlier

import ctypes

CLOCK_REALTIME = 0

class timespec(ctypes.Structure):
    _fields_ = [
        ('tv_sec', ctypes.c_int64), # seconds, https://stackoverflow.com/q/471248/1672565
        ('tv_nsec', ctypes.c_int64), # nanoseconds
    ]

clock_gettime = ctypes.cdll.LoadLibrary('libc.so.6').clock_gettime
clock_gettime.argtypes = [ctypes.c_int64, ctypes.POINTER(timespec)]
clock_gettime.restype = ctypes.c_int64


def time_ns():
    tmp = timespec()
    ret = clock_gettime(CLOCK_REALTIME, ctypes.pointer(tmp))
    if bool(ret):
        raise OSError()
    return tmp.tv_sec * 10 ** 9 + tmp.tv_nsec


def mytimeit(func, n=1):
    """A decorator to measure runtime of a function in nanoseconds"""
    def wrapper(*args, **kwargs):
        start = time_ns()
        res = func(*args, **kwargs)
        end = time_ns()
        print("Runtime[{}]: {} nsec".format(func.__name__, end-start))
        return res
    return wrapper


def mdrange_my(*ranges):
    """
    Generates all combinations (n-tuples)
    >>> ranges = [(0, 3), (10, 12), (101, 104)]
    >>> for x,y,z in mdrange(*ranges):
    >>>   ...
    """
    assert ranges, "Cannot be empty"
    head, tails = ranges[0], ranges[1:]
    if not tails:
        for x in range(*head):
            yield (x,)
    else:
        for x in range(*head):
            for y in mdrange(*tails):
                yield (x, *y)


def mdrange(*ranges):
    # TODO: add support for mdrange(5, 6) where range(5) and range(6)
    rngs = [rng if isinstance(rng, range) else range(*rng) for rng in ranges]
    yield from itertools.product(*rngs)


def prod(numbers: List[int]):
    return functools.reduce(lambda a, b: a*b, numbers, 1)


def listfold(lst: List[Any], width: int) -> List[List[Any]]:
    """Folds (reshapes) a list into 2 dimentional matrix by folding at
    given position `width`. each row will contain at most `width` items
    """
    reshaped = []
    for ridx in range(len(lst) // width):
        start = ridx * width
        reshaped.append(lst[start:start+width])
    return reshaped


def test2str(success, expected, actual):
    lines = []
    if "\n" in str(expected) or "\n" in str(actual):
        lines.append(str(success))
        if success:
            lines += ["Expected and Actual:", str(expected)]
        else:
            lines += ["Expected:", str(expected), "Actual:", str(actual)]
    else:
        lines.append(f"{success} {expected} {actual}")
    return "\n".join(lines)


def run_tests(
    day: str,
    tests: List[Tuple], # (input, expected-part-1, expected-part-2)
    solve_p1: Callable = None,
    solve_p2: Callable = None
):
    print(f"--- Tests day {day} ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if solve_p1 and exp1 is not None:
            res1 = solve_p1(deepcopy(inp))
            print(f"T.{tid}.p1:", test2str(res1 == exp1, exp1, res1))

        if solve_p2 and exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T.{tid}.p2:", test2str(res2 == exp2, exp2, res2))


def run_real(
    day: str,
    tests: List[Tuple], # (input, expected-part-1, expected-part-2)
    solve_p1: Callable = None,
    solve_p2: Callable = None
):
    for tid, (inp, exp1, exp2) in enumerate(tests):
        print(f"--- Day {day} p.1 ---")
        res1 = solve_p1(deepcopy(inp))
        print(test2str(exp1 == res1, exp1, res1))

        print(f"--- Day {day} p.2 ---")
        res2 = solve_p2(inp)
        print(test2str(exp2 == res2, exp2, res2))


class Vector(object):

    def __init__(self, values: Iterable = None):
        self.values = list(values or [])

    def __hash__(self):
        return hash(tuple(self.values))

    def __add__(self, other: Union["Vector", Iterable]) -> "Vector":
        return self.pairwise(other, lambda a, b: a+b)

    def __sub__(self, other: Union["Vector", Iterable]) -> "Vector":
        return self.pairwise(other, lambda a, b: a-b)

    def pairwise(
        self,
        other: Union["Vector", Iterable],
        func: Callable   # functools.reduce()
    ) -> "Vector":
        assert len(self) == len(other), (
            f"Length mismatch: {len(self)} vs. {len(other)}"
        )
        values = [functools.reduce(func, pair) for pair in zip(self, other)]
        return self.__class__(values)

    # def __getattr__(self, name: str):
    #     print("method", name, type(name))

    def __abs__(self):
        # TODO: implement generically via __getattr__
        return self.__class__(abs(v) for v in self)

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def __repr__(self):
        return "<{}: values={}>".format(self.__class__.__name__, self.values)

    def __str__(self):
        return str(tuple(self.values))

    def __getitem__(self, idx: int):
        return self.values[idx]

    def __eq__(self, other: "Vector"):
        return tuple(self.values) == tuple(other)


class Point(Vector):
    """for purposes of clearer naming"""

    def __init__(self, *coords: Union[int, List[int]]):
        if isinstance(coords[0], (list, tuple, type(self))):
            super().__init__(*coords)
        else:
            super().__init__(coords)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    def l1_dist(self, other: 'Point') -> int:
        """L1 distance aka Manhattan distance"""
        return sum(*abs(self - other))

    def __lt__(self, other: 'Point'):
        return self.x < other.x or self.x == other.x and self.y < other.y


class Matrix(object):
    """Matrix

    Implementing it for fun.
    Not as good as pandas dataframe
    """
    def __init__(self, *args):
        if len(args) == 1:
            # from List[List]
            shape = len(args[0]), len(args[0][0])
            self.__init__(*shape)
            self.values = args[0]  # TODO: make a copy of 2 levels
        elif len(args) > 1:
            n_rows, n_cols = args[:2]
            value = args[2] if len(args) > 2 else 0
            self.values = [[value] * n_cols for _ in range(n_rows)]

    def shape(self):
        return (len(self.values), len(self.values[0]))

    def _is_in_span(self, xy: Tuple[int, int]) -> bool:
        """Check that given coordinate `xy` exists in the matrix"""
        n_rows, n_cols = self.shape()
        x, y = xy
        return 0 <= x < n_rows and 0 <= y < n_cols

    def __getitem__(self, xy: Tuple[int, int]):
        if self._is_in_span(xy):
            x, y = xy
            return self.values[x][y]
        raise IndexError(f"Matrix index {xy} out of range")

    def __setitem__(self, xy: Tuple[int, int], newval: Any):
        if self._is_in_span(xy):
            x, y = xy
            self.values[x][y] = newval
        else:
            raise IndexError(f"Matrix index {xy} out of range")

    def get(self, xy: Tuple[int, int], default = None):
        if self._is_in_span(xy):
            x, y = xy
            return self.values[x][y]
        else:
            return default

    def __str__(self):
        return "\n".join([str(row) for row in self.values])
