"""Conveyerbelt-like operations with deques and callables.
"""
from collections import deque


class Deque(deque):
    def __rshift__(self, other):
        if callable(other):
            return other(self.pop())
        other.appendleft(self.pop())
        return other

    def __lshift__(self, other):
        if self and callable(self[-1]):
            f = self.pop()
        else:
            f = lambda x: x

        if callable(other):
            self.append(other)
            return self

        if isinstance(other, deque):
            self.append(f(other.popleft()))
            return other

        self.append(f(other))
        return self

    def __rrshift__(self, other):
        if self and callable(self[0]):
            f = self.popleft()
        else:
            f= lambda x: x

        if callable(other):
            self.appendleft(other)
            return self

        self.appendleft(f(other))
        return self

    def __rlshift__(self, other):
        self.appendleft(other(self.popleft()))
        return self


if __name__ == "__main__":

    a, b, c = (Deque() for _ in range(3))

    a << 1 << 2 << 3
    b << 4 << 5 << 6
    c << 7 << 8 << 9

    print(a, b, c)

    a >> b >> c

    print(a, b, c)

    a >> b << c

    print(a, b, c)
