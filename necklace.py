from collections import deque

class Necklace:
    """Necklaces are tuples that "wrap-around", e.g., (1,2,3,4) == (3,4,1,2) is
    true, but (1,2,3,4) == (1,2,4,3) is not.
    To facilitate fast comparison of Necklaces, they store their
    canonical form (specifically, the least shift).
    """
    def __init__(self, items):
        super().__setattr__('_items', deque(items))

        super().__setattr__('_least', self._items.copy())  # least shift
        for _ in range(len(self)):
            self._items.rotate()
            if self._items < self._least:
                super().__setattr__('_least', self._items.copy())

    def __len__(self):
        return len(self._items)

    def __eq__(self, other):
        if not isinstance(other, Necklace):
            return NotImplemented
        return self._least == other._least

    def __iter__(self):
        yield from self._items

    def __repr__(self):
        return f'{type(self).__name__}([{", ".join(map(repr, self))}])'

    def __setattr__(self, attr, val):
        raise AttributeError('Necklace is immutable')

    def __getitem__(self, index):
        return self._items[index]

    def rotate(self, n=1):
        self._items.rotate(n)

    def copy(self):
        copy = type(self)(())
        super(type(self), copy).__setattr__('_items', self._items.copy())
        super(type(self), copy).__setattr__('_least', self._least)
        return copy