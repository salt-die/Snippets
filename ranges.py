"""Continuous Range implementation -- Along with a dictionary-like object for quickly finding
which Range contains a key.
"""
# TODO: Implement __invert__, symmetric difference, subset, superset
#  ...: Finish RangeSet implementation:
#  ...:    All Range operations should be implemented on RangeSet, but care needs
#  ...:    needs to be taken to stay O(n) where possible.
from bisect import bisect_left, bisect_right, insort
from contextlib import suppress
from functools import wraps

class ImmutableError(Exception): pass

class Immutable:
    def __setattr__(self, attr, value):
        raise ImmutableError(f"cannot assign to '{attr}'")

class INF(Immutable):
    def __lt__(self, other): return False
    def __gt__(self, other): return True
    def __neg__(self): return MINUS_INF
    def __repr__(self): return '∞'
    def __hash__(self): return hash(float('inf'))

class MINUS_INF(Immutable):
    def __lt__(self, other): return True
    def __gt__(self, other): return False
    def __neg__(self): return INF
    def __repr__(self): return '-∞'
    def __hash__(self): return hash(-float('inf'))

class RangeBase(Immutable):
    """Annotative base class."""

class EMPTY_RANGE(RangeBase):
    def __contains__(self, other): return False
    def intersects(self, other): return False
    def __lt__(self, other): return True
    def __gt__(self, other): return True
    def __or__(self, other): return other
    def __and__(self, other): return self
    def __repr__(self): return '∅'

INF = INF()
MINUS_INF = MINUS_INF()
EMPTY_RANGE = EMPTY_RANGE()

def ensure_order(func):
    """Raise error if other isn't an instance of RangeBase and switch other, self if other < self.
    """
    @wraps(func)
    def wrapper(self, other):
        if not isinstance(other, RangeBase):
            raise ValueError(f'{other} not an instance of Range')

        if other < self:
            self, other = other, self
        return func(self, other)
    return wrapper

def from_string(str_):
    start, end = str_[1:-1].split(',')
    start = start.strip()
    end = end.strip()
    if start == '-inf':
        start = -INF
        start_inc = False
    else:
        start = int(start) if start.isdigit() else float(start)
        start_inc = str_[0] == '['

    if end == 'inf':
        end = INF
        end_inc = False
    else:
        end = int(end) if end.isdigit() else float(end)
        end_inc = str_[-1] == ']'
    return start, end, start_inc, end_inc

class Range(RangeBase):
    __slots__ = 'start', 'end', 'start_inc', 'end_inc', '_cmp', '_hash'

    def __init__(self, start=None, end=None, /, start_inc=True, end_inc=False):
        # Try to construct from string
        with suppress(TypeError, ValueError, IndexError):
            start, end, start_inc, end_inc = from_string(start)

        if start is None:
            start = MINUS_INF
            start_inc = False
        if end is None:
            end = INF
            end_inc = False

        try:
            if start > end:
                start, end = end, start
                start_inc, end_inc = end_inc, start_inc
            elif start == end and not (start_inc and end_inc):
                raise ValueError('range must be inclusive if start equals end')
        except TypeError:
            raise TypeError('start must be comparable to end')

        cmp = (start, int(not start_inc)), (end, int(end_inc))
        hash_ = hash(cmp)

        for name, val in zip(self.__slots__, (start, end, start_inc, end_inc, cmp, hash_)):
            super(Immutable, type(self)).__setattr__(self, name, val)

    def __lt__(self, other):
        if isinstance(other, Range):
            return self._cmp < other._cmp

        try:
            return self.end < other or not self.end_inc and self.end == other
        except TypeError:
            raise TypeError(f"'<{type(other).__name__}>' not comparable to {type(self.end).__name__}")

    def __gt__(self, other):
        if isinstance(other, Range):
            return other < self

        try:
            return self.start > other or not self.start_inc and self.start == other
        except TypeError:
            raise TypeError(f"'<{type(other).__name__}>' not comparable to {type(self.start).__name__}")

    def __eq__(self, other):
        if not isinstance(other, Range):
            return False
        return self._cmp == other._cmp

    def __hash__(self):
        return self._hash

    def __contains__(self, value):
        """Return true if value is in the range."""
        try:
            return (self.start < value < self.end
                    or self.start == value and self.start_inc
                    or self.end == value and self.end_inc)
        except TypeError:
            raise TypeError(f"'in <{type(self).__name__}>' requires type comparable to "
                            f"{type(self.start).__name__} as left operand, not {type(value).__name__}")

    @ensure_order
    def continues(self, other):
        """Return true if either self.end == other.start or self.start == other.end
        and one point is inclusive and the other is exclusive.
        """
        return self.end_inc != other.start_inc and self.end == other.start

    @ensure_order
    def intersects(self, other):
        """Return true if the intersection with 'other' isn't empty."""
        return other.start in self and not self.continues(other)

    @ensure_order
    def __or__(self, other):
        """Returns union of two Ranges."""
        if self.end > other:
            return self

        if not (self.intersects(other) or self.continues(other)):
            return RangeSet(self, other)

        return Range(self.start, other.end, self.start_inc, other.end_inc)

    @ensure_order
    def __and__(self, other):
        """Returns intersection of two Ranges."""
        if self.end > other:
            return other

        if not self.intersects(other):
            return EMPTY_RANGE

        return Range(other.start, self.end, other.start_inc, self.end_inc)

    def __repr__(self):
        return f'{"(["[self.start_inc]}{self.start}, {self.end}{")]"[self.end_inc]}'


class RangeDict:
    def __init__(self, dict_=None):
        self._ranges = []
        self._range_to_value = {}

        if dict_ is not None:
            for key, value in dict_.items():
                self[key] = value

    def __setitem__(self, key, value):
        """Keep ranges sorted as we insert them. Raise ValueError if key is not disjoint to its neighbors.
        """
        if key not in self._range_to_value:

            i = bisect_right(self._ranges, key)

            with suppress(IndexError):
                if self._ranges[i].intersects(key) or self._ranges[i - 1].intersects(key):
                    raise ValueError(f'{key} is not disjoint from other Ranges')
            self._ranges.insert(i, key)

        self._range_to_value[key] = value

    def __getitem__(self, key):
        """Binary search the ranges for one that may contain the key."""
        ranges = self._ranges
        values = self._range_to_value
        while ranges:
            i = bisect_left(ranges, key)
            if key in ranges[i]:
                return values[ranges[i]]

            ranges = ranges[i + 1:]
            if not ranges:
                break

            i = bisect_right(ranges, key) - 1
            if key in ranges[i]:
                return values[ranges[i]]

            ranges = ranges[:i]

        raise KeyError(key)

    def __repr__(self):
        return f'{self.__class__.__name__}({self._range_to_value})'


class RangeSet:
    """A collection of mutually disjoint Ranges."""
    def __init__(self, *ranges):
        NotImplemented


if __name__ == '__main__':
    r = RangeDict({Range('[90, 100]'): 'A',
                   Range(  80,  90  ): 'B',
                   Range(  70,  80  ): 'C',
                   Range(  60,  70  ): 'D',
                   Range(   0,  60  ): 'F'})
    assert r[85] == 'B'
    assert r[90] == 'A'
    assert r[ 0] == 'F'

    a = Range(0, 1)
    b = Range(1, 2)
    c = Range(0, 2)

    assert a | c == c
    assert a & c == a

    assert a | b == c
    assert a & b == EMPTY_RANGE