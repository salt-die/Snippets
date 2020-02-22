"""Taken from somewhere on the Stack."""
def partition(collection):
    """Generate all partitions of collection"""
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

def partitions(n, m=None):
    """Generate all integer partitions of n with part size no bigger than m."""
    if m is None or m >= n:
        yield [n]
        start = n - 1
    else:
        start = m

    for m0 in range(start, 0, -1):
        for subpartition in partitions(n - m0, m0):
            yield [size] + subpartition