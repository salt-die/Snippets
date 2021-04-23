from contextlib import contextmanager


class TailParams(Exception):
    ...


class tail_recursive:
    def __init__(self, func):
        self.func = func

    @classmethod
    @contextmanager
    def tail_call(cls):
        cls.__call__, tmp = cls.__tail__, cls.__call__
        try:
            yield
        finally:
            cls.__call__ = tmp

    def __call__(self, *args, **kwargs):
        with self.tail_call():
            while True:
                try:
                    return self.func(*args, **kwargs)
                except TailParams as tp:
                    args, kwargs = tp.args

    def __tail__(self, *args, **kwargs):
        raise TailParams(args, kwargs)


if __name__ == "__main__":
    @tail_recursive
    def fib(n, a=0, b=1):
        if n == 0:
            return a
        if n == 1:
            return b
        return fib(n - 1, b, a + b)

    print(fib(2000))