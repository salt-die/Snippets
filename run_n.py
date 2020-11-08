"""I'm unsure of the best way to let a decorator determine if the function it decorates is
defined inside a class or not.  This is one hack-y solution:  see if the first parameter of the function is `self`.
"""

from collections import Counter
from functools import wraps
from inspect import signature

def run_n(n):
    """Decorator that allows a function or method to only run n times."""
    def deco(f):
        instance_run_counts = Counter()

        # determine if function was defined in a class
        if (params := signature(f).parameters) and next(iter(params)) == 'self':
            @wraps(f)
            def wrapper(*args, **kwargs):
                if args:
                    if instance_run_counts[id(args[0])] < n:
                        instance_run_counts[id(args[0])] += 1
                        return f(*args, **kwargs)
                else:
                    # Run from class
                    raise TypeError(f"{f.__name__}() missing 1 required positional argument 'self'")

        else:
            @wraps(f)
            def wrapper(*args, **kwargs):
                if wrapper.nruns < n:
                    wrapper.nruns += 1
                    return f(*args, **kwargs)
            wrapper.nruns = 0

        return wrapper

    return deco
