from random import choice


class Dictch(dict):
    """Dict with choice.  Dictch."""
    __slots__ = '_item_to_pos', '_items'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._item_to_pos = {item: i for i, item in enumerate(self)}
        self._items = list(self)

    def __setitem__(self, key, value):
       if key not in self:
           self._items.append(key)
           self._item_to_pos[key] = len(self._items) - 1
       return super().__setitem__(key, value)

    def __delitem__(self, key):
        super().__delitem__(key)
        position = self._item_to_pos.pop(key)
        last_item = self._items.pop()
        if position != len(self._items):
            self._items[position] = last_item
            self._item_to_pos[last_item] = position

    def choose(self):
        return choice(self._items)