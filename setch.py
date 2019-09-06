# -*- coding: utf-8 -*-
"""
Setch is a portmanteau of set and CHoice.

If one finds oneself needing to choose items from sets at random, constantly
converting those sets to lists can significantly slow down your program.  This
class is set-like, but allows one to choose an item at random from it with no
conversion necessary.
"""
from random import choice

class Setch:
    """
    A set-like object that allows one to choose an item at random from it.
    """
    def __init__(self, *items):
        self._item_to_position = {}
        self.items = []
        for item in items:
            self.add(item)


    def add(self, item):
        """
        Add an item to Setch.
        """
        if item in self._item_to_position:
            return
        self.items.append(item)
        self._item_to_position[item] = len(self.items)-1

    def remove(self, item):
        """
        Remove item from setch if possible, otherwise do nothing.
        """
        try:
            position = self._item_to_position.pop(item)
        except KeyError:
            return
        last_item = self.items.pop()
        if position != len(self.items):
            self.items[position] = last_item
            self._item_to_position[last_item] = position

    def choose(self):
        """
        Return a random item.
        """
        if not self.items:
            return None
        return choice(self.items)

    def __add__(self, other):
        result = Setch(*self, *other)
        return result

    def __iadd__(self, other):
        self = self + other
        return self

    def __sub__(self, other):
        result = Setch(*self)
        for item in other:
            result.remove(item)
        return result

    def __isub__(self, other):
        self = self - other
        return self

    def __eq__(self, other):
        return set(self.items) == set(other.items)

    def __iter__(self):
        return iter(self.items)

    def __repr__(self):
        return '{' + repr(self.items)[1:-1] + '}'
