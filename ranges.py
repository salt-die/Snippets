from bisect import bisect_left, bisect_right, insort
from functools import wraps


class ImmutableError(Exception): pass


class EmptyRange:
    def __contains__(self, other):
        return False
    def __setattr__(self, attr, value):
        raise ImmutableError(f"cannot assign to '{attr}'")
    def intersects(self, other):
        return False
    def __repr__(self):
        return '∅'


EMPTYRANGE = EmptyRange()

def ensure_order(func):
    """If not self < other, call other.func(self)."""
    @wraps(func)
    def wrapper(self, other):
        if other < self:
            return getattr(other, func.__name__)(self)
        return func(self, other)
    return wrapper


class Range:
    def __init__(self, start, end=None, start_inc=True, end_inc=False):
        # Start is a string
        if end is None:
            start_inc = start[0] == '['
            end_inc = start[-1] == ']'
            start, end = map(float, start[1:-1].split(','))

        try:
            if start > end:
                raise ValueError('start must be less than or equal to end')
            elif start == end and not start_inc and not end_inc:
                raise ValueError('range must be inclusive if start equals end')
        except TypeError:
            raise TypeError('start must be comparable to end')

        self.__dict__['start'] = start
        self.__dict__['end'] = end
        self.__dict__['start_inc'] = start_inc
        self.__dict__['end_inc'] = end_inc
        self.__dict__['_cmp'] = (self.start, not self.start_inc), (self.end, self.end_inc)

    def __lt__(self, other):
        if isinstance(other, Range):
            return self._cmp < other._cmp

        try:
            return self.end < other
        except TypeError:
            raise TypeError(f"'<{type(other).__name__}>' not comparable to {type(self.end).__name__}")

    def __gt__(self, other):
        if isinstance(other, Range):
            return other < self

        try:
            return self.start > other
        except TypeError:
            raise TypeError(f"'<{type(other).__name__}>' not comparable to {type(self.start).__name__}")

    def __eq__(self, other):
        if not isinstance(other, Range):
            return False
        return self._cmp == other._cmp

    def __hash__(self):
        # cache the hash
        if not hasattr(self, '_hash'):
            self.__dict__['_hash'] = hash(self._cmp)
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

    def __setattr__(self, attr, value):
        """Force immutability."""
        raise ImmutableError(f"cannot assign to '{attr}'")

    @ensure_order
    def intersects(self, other):
        """Return true if the intersection with 'other' isn't empty."""
        return other.start < self.end or self.meets(other)

    @ensure_order
    def meets(self, other):
        """Return true if either self.start == other.end or self.end == other.start
        and start and end are inclusive.
        """
        return self.end == other.start and self.end_inc and other.start_inc

    @ensure_order
    def continues(self, other):
        """Return true if either self.end == other.start or self.start == other.end
        and one point is inclusive and the other is exclusive.
        """
        return self.end == other.start and self.end_inc != other.start_inc

    @ensure_order
    def __or__(self, other):
        """Returns union of two Ranges."""
        if not self.intersects(other) and not other.continues(self):
            return RangeSet(self, other)

        if self.end > other.end or self.end == other.end and self.end_inc:
            return self

        return Range(self.start, other.end, self.start_inc, other.end_inc)

    @ensure_order
    def __and__(self, other):
        """Returns intersection of two Ranges."""
        if not self.intersects(other):
            return EMPTYRANGE

        if self.end > other.end or self.end == other.end and self.end_inc:
            return other

        return Range(other.start, self.end, other.start_inc, self.end_inc)


    def __repr__(self):
        return f'{"(["[self.start_inc]}{self.start}, {self.end}{")]"[self.end_inc]}'


class RangeDict:
    def __init__(self, dict_):
        self._ranges = []
        self._range_to_value = {}

        for key, value in dict_.items():
            self.__setitem__(key, value)

    def __setitem__(self, key, value):
        if key not in self._range_to_value:
            insort(self._ranges, key)
        self._range_to_value[key] = value

    def __getitem__(self, key):
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
    def __init__(self, *ranges):
        NotImplemented


if __name__ == '__main__':
    r = RangeDict({Range('[90, 100]'): 'A',
                   Range( '[80, 90)'): 'B',
                   Range( '[70, 80)'): 'C',
                   Range( '[60, 70)'): 'D',
                   Range(  '[0, 60)'): 'F'})