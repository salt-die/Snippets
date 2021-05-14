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

### Following recipes from
### https://stackoverflow.com/questions/10035752/elegant-python-code-for-integer-partitioning
### Credit to David Vanderschel

def partitions(n, m=None):
    """Generate all integer partitions of n with part size no bigger than m."""
    if m is None or m >= n:
        yield [n]
        start = n - 1
    else:
        start = m

    for m0 in range(start, 0, -1):
        for subpartition in partitions(n - m0, m0):
            yield [m0] + subpartition

def sized_partitions(n, k, m=None):
    """Partition n into k parts with a max part of m."""
    if k == 1:
        yield [n]
        return

    start = n - k + 1
    if not (m is None or m > start):
        start = m

    for m0 in range(start, (n - 1) // k, -1):
        for subpartition in sized_partitions(n - m0, k - 1, m0):
            yield [m0] + subpartition

def partitions_upto(n, max_val=100000, max_len=100000):
    """ generator of partitions of sum with limits on values and length """
    if n <= max_val:
        yield [n]

    for m0 in range(min(n - 1, max_val), max(0, (n - 1) // max_len), -1):
        for subpartition in partitions_upto(n - m0, m0, max_len - 1):
            yield [m0] + subpartition
