from collections import deque


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
        """Return the nth item in peeked with n `_`s"""
        n = attr.count('_')
        if n != len(attr):
            return super().__getattribute__(attr)
        return self.peek(n)[-1]

    def peek(self, n=None, default=NULL):
        if n is None:
            return self.peek(n=1, default=default)[0]

        while len(self.peeked) < n:
            try:
                self.peeked.append(next(self.iterable))
            except StopIteration:
                if default is NULL: raise StopIteration
                self.peeked.append(default)

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
            items = ', '.join(map(str, self.peek(3))) + '...'
        return f'peekable([{items}])'