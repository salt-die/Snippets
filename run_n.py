from functools import singledispatch, wraps
from types import MethodType, FunctionType


def run_n(n):
    """Decorator that allows a function or method to only run n times."""
    @singledispatch
    def deco(f: FunctionType):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if wrapper.nruns < n:
                wrapper.nruns += 1
                return f(*args, **kwargs)
        wrapper.nruns = 0
        return wrapper

    @deco.register
    def _(f: MethodType):
        instance_run_counts = Counter()

        @wraps(f)
        def wrapper(self, *args, **kwargs):
            if instance_run_counts[(i := id(self))] < n:
                instance_run_counts[i] += 1
                return f(self, *args, **kwargs)

        return wrapper

    return deco