#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Numpy version of itertools.combinations from:
https://stackoverflow.com/questions/42138681/faster-numpy-solution-instead-of-itertools-combinations

Example:
>>> arr = np.array(['a', 'b', 'c', 'd', 'e'])
>>> comb(arr, 3)  #Combinations of 3 items

array([['a', 'b', 'c'],
       ['a', 'b', 'd'],
       ['a', 'b', 'e'],
       ['a', 'c', 'd'],
       ['a', 'c', 'e'],
       ['a', 'd', 'e'],
       ['b', 'c', 'd'],
       ['b', 'c', 'e'],
       ['b', 'd', 'e'],
       ['c', 'd', 'e']], dtype='<U1')
"""
import numpy as np

def comb(array, k):
    n = len(array)
    a = np.ones((k, n-k+1), dtype=int)
    a[0] = np.arange(n-k+1)
    for i in range(1, k):
        reps = (n-k+i) - a[i-1]
        a = np.repeat(a, reps, axis=1)
        ind = np.add.accumulate(reps)
        a[i, ind[:-1]] = 1-reps[1:]
        a[i, 0] = i
        a[i] = np.add.accumulate(a[i])
    return array[a.T]