
from typing import List, Union, Tuple, Optional, Callable


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


def minmax(numbers: List[int]) -> Tuple[int, int]:
    """Return min and max values from given list of integers"""
    return (min(numbers), max(numbers))

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


def run_tests(
    day: str,
    tests: List[Tuple], # (input, expected-part-1, expected-part-2)
    solve_p1: Callable = None,
    solve_p2: Callable = None
):
    print(f"--- Tests day {day} ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if solve_p1 and exp1 is not None:
            res1 = solve_p1(inp)
            print(f"T.{tid}.p1:", res1 == exp1, exp1, res1)

        if solve_p2 and exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T.{tid}.p2:", res2 == exp2, exp2, res2)


def run_real(
    day: str,
    tests: List[Tuple], # (input, expected-part-1, expected-part-2)
    solve_p1: Callable = None,
    solve_p2: Callable = None
):
    for tid, (inp, exp1, exp2) in enumerate(tests):
        print(f"--- Day {day} p.1 ---")
        res1 = solve_p1(inp)
        print(exp1 == res1, exp1, res1)

        print(f"--- Day {day} p.2 ---")
        res2 = solve_p2(inp)
        print(exp2 == res2, exp2, res2)
