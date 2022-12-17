
from typing import Union, Tuple, List, Optional


class BrokenLine(object):
    """
    A line segment starting and endint at given positions `start` and `end`.
    Both ends are included.
    It can be continuous or discontinous. The latter consists if a number of
    segments (`parts`), each with its own `start` and `end` values.

    TODO: solve it with a sparse matrix from scipy
    """
    DEBUG = False

    def __init__(self, start: int, end: int):
        # start and end are included
        self.parts: List[Tuple[int, int]] = [(start, end)]

    def __len__(self) -> int:
        """Length of a BrokenLine is the sum of lenths of its subsegments."""
        return sum(end-start+1 for start, end in self.parts)

    def _dprint(self, *msgs):
        if self.DEBUG:
            print(*msgs)

    def erase_at(self, pos: int):
        """Delete given position `pos` from the line, if it exists.
        Deletion results in then that contsins `pos` being split in two.
        """
        idx = self._index_of(pos)
        if self.DEBUG:
            p = None if idx is None else self.parts[idx]
            print(f"Target {pos} found at [{idx}] = {p}")
        if idx is not None:
            start, end = self.parts[idx]
            left, right = (start, pos-1), (pos+1, end)
            self._dprint("Left/right", left, right)
            self.parts[idx] = right
            self.parts.insert(idx, left)

    def __isub__(self, other: Union[int, Tuple[int, int]]):
        """Erase `other` from current line. `other` can be one of:
        * int -- a single point will be erased
        * Tuple of two ints -- remove a subsegment
        """
        if isinstance(other, int):
            # subtract/erase a single point
            self.erase_at(other)
        elif isinstance(other, (tuple, list)):
            # subtract another segment
            self._dprint("subtracting segment", other)
            start, end = other
            self.erase_at(start)
            self.erase_at(end)
            self._dprint(f"after splitting: {self.parts}")
            # remove all subsegments that are completely contained in `other`
            self.parts = [
                part
                for part in self.parts
                if not all(start <= pos <= end for pos in part)
            ]
        else:
            raise ValueError(
                f"Not supported type of argument {type(other)}"
            )
        return self

    def _index_of(self, value: int) -> Optional[int]:
        """find index of the segment that contains given value.
        The value can be either within the segment or at any of its ends.
        If not found, return None
        """
        for idx, part in enumerate(self.parts):
            if part[0] <= value <= part[1]:
                return idx
        return None

    def positions(self) -> List[int]:
        """Return a list of ints that correspond to all positions that
        exist on the line.
        """
        points = []
        for start, end in self.parts:
            points.extend(range(start, end+1))
        return points

    def __repr__(self):
        return "<{}: length={}, parts={}>".format(
            self.__class__.__name__, len(self), self.parts)
