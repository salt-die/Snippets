"""
Setch is a portmanteau of set and choice.  A setch is set-like object (containment is O(1)) except
one can pick items at random from the set without converting it to a list. This is a multiset
implementation of a setch.

Note most list operations are O(1) except for indexing in `remove`.
"""
from collections import defaultdict
from random import choice

class MultiSetch:
    def __init__(self, *items):
        self._item_to_position = defaultdict(list)
        self.items = []
        for item in items:
            self.add(item)

    def add(self, item):
        self.items.append(item)
        self._item_to_position[item].append(len(self.items) - 1)

    def remove(self, item):
        position = self._item_to_position[item].pop()
        last_item = self.items.pop()
        if position != len(self.items):
            self._item_to_position[last_item].pop()
            self.items[position] = last_item
            self._item_to_position[last_item].append(position)

    def choose(self):
        return choice(self.items)

    def pop(self):
        """Pop a random item."""
        item = self.choose()
        self.remove(item)
        return item

    def __len__(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self._item_to_position

    def __iter__(self):
        return iter(self.items)

    def __repr__(self):
        return f'MultiSetch({{{", ".join(map(str, self.items))}}})'