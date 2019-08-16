#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate all partitions of an iterable.
Version one returns a generator, version 2 returns a list.
Taken from somewhere on the Stack.
"""
def partition(collection):
    if len(collection) == 1:
        yield [collection]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[first] + subset] + smaller[n+1:]
        # put `first` in its own subset
        yield [[first]] + smaller

def partition2(collection):
    if len(collection) == 1:
        return [[collection]]

    first = collection[0]
    subparts = []
    for smaller in partition2(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            subparts.append(smaller[:n] + [[first] + subset] + smaller[n+1:])
        # put `first` in its own subset
        subparts.append([[first]] + smaller)
    return subparts
