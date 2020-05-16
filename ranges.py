from bisect import bisect_left, bisect_right, insort

class ImmutableError(Exception): pass

class Range:
    def __init__(self, start, end=None, start_inc=True, end_inc=False):
        # Start is a string
        if end is None:
            start_inc = start[0] == '['
            end_inc = start[-1] == ']'
            start, end = map(float, start[1:-1].split(','))

        self.__dict__['start'] = start
        self.__dict__['end'] = end
        self.__dict__['start_inc'] = start_inc
        self.__dict__['end_inc'] = end_inc

    def __lt__(self, other):
        if isinstance(other, Range):
            return ((self.start, not self.start_inc), (self.end, self.end_inc)) \
                   < ((other.start, not other.start_inc), (other.end, other.end_inc))
        return self.end < other

    def __gt__(self, other):
        if isinstance(other, Range):
            return other < self
        return self.start > other

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(tuple(self.__dict__.values()))

    def __contains__(self, value):
        return (self.start < value < self.end
                or self.start == value and self.start_inc
                or self.end == value and self.end_inc)

    def __setattr__(self, attr, value):
        raise ImmutableError(f"cannot assign to '{attr}'")

    def __or__(self, other):
        """For non-disjoint ranges only. Returns union of two Ranges."""
        if other.start < self.start or self.start == other.start and self.end > other.end:
            return other | self

        if self.start == other.start:
            return Range(self.start, other.end, self.start_inc or other.start_inc, other.end_inc)

        if self.end > other.end:
            return self

        if self.end == other.end:
            return Range(self.start, self.end, self.start_inc, self.end_inc or other.end_inc)

        if self.end > other.start:
            return Range(self.start, other.end, self.start_inc, other.end_inc)

        if self.end == other.start:
            return Range(self.start, other.end, self.start_inc, self.start_inc or other.start_inc)

        raise ValueError('Ranges disjoint')

    def __repr__(self):
        return f'{"(["[self.start_inc]}{self.start}, {self.end}{")]"[self.end_inc]}'


class RangeDict:
    def __init__(self, dict_):
        self._ranges = []
        self._range_to_value = {}

        for key, value in dict_.items():
            self.__setitem__(key, value)

    def __setitem__(self, key, value):
        if key not in self._range_to_value: insort(self._ranges, key)
        self._range_to_value[key] = value

    def __getitem__(self, key):
        ranges = self._ranges
        values = self._range_to_value
        while ranges:
            i = bisect_left(ranges, key)
            if key in ranges[i]: return values[ranges[i]]

            ranges = ranges[i + 1:]
            if not ranges: break

            i = bisect_right(ranges, key) - 1
            if key in ranges[i]: return values[ranges[i]]

            ranges = ranges[:i]
        raise KeyError(key)

    def __repr__(self):
        return f'{self.__class__.__name__}({self._range_to_value})'

if __name__ == '__main__':
    r = RangeDict({Range('[90, 100]'): 'A',
                   Range( '[80, 90)'): 'B',
                   Range( '[70, 80)'): 'C',
                   Range( '[60, 70)'): 'D',
                   Range(  '[0, 60)'): 'F'})