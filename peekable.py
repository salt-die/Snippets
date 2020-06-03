from collections import deque
from functools import partial

NULL = type('', (), {})()  # None is a valid default value, so we use this for no default.

class peekable:
    def __init__(self, iterable):
        self.iterable = iter(iterable)
        self.peeked = deque()

    def __iter__(self): return self

    def __next__(self):
        if self: return self.peeked.popleft()
        raise StopIteration

    def __getattr__(self, attr):
        """Return the nth item in peeked with n  _'s, e.g., `.peek(2)` equivalent to `.__`"""
        n = attr.count('_')
        if n != len(attr):
            return super().__getattribute__(attr)
        return self.peek(n)[-1]

    def peek(self, n=None, default=NULL):
        if n is None:
            return self.peek(n=1, default=default)[0]

        next_ = partial(next, self.iterable) if default is NULL else partial(next, self.iterable, default)

        while len(self.peeked) < n:
            self.peeked.append(next_())

        return tuple(map(self.peeked.__getitem__, range(n)))

    def __bool__(self):
        """Return False if peeked is empty and iterable is exhausted."""
        try:
            self.peek(1)
        except StopIteration:
            return False
        return True

    def __repr__(self):
        try:
            self.peek(4)
        except StopIteration:
            items = ", ".join(map(str, self.peeked))
        else:
            items = ', '.join(map(str, self.peek(3))) + ', ...'
        return f'peekable([{items}])'