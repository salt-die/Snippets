# -*- coding: utf-8 -*-
class CyclicTuple:
    """
    CyclicTuples are tuples that "wrap-around", e.g., (1,2,3,4) == (3,4,1,2) is
    true, but (1,2,3,4) == (1,2,4,3) is not.

    To facilitate fast comparison of CyclicTuples, CyclicTuples store their
    canonical form (specifically, the least shift) -- fast comparison of
    shifts is what necessitated this class.
    """
    def __init__(self, *items):
        self.__unshifted = tuple(items)
        self.__canonical = min(items[i:] + items[:i]\
                               for i,_ in enumerate(items))

    def __repr__(self):
        return repr(self.__unshifted)

    def __eq__(self, other):
        try:
            return self.__canonical == other._CyclicTuple__canonical
        except AttributeError:
            return False

    def index(self, item):
        return self.__unshifted.index(item)

    #Return a list of the indices of all occurences of an item in self
    def indices(self, item):
        return [i for i, n in enumerate(self.__unshifted) if n==item]

    #Return a list of unique items in self -- items in no particular order
    def items(self):
        return list({*self.__unshifted})

    def __getitem__(self, key):
        return self.__unshifted[key]
