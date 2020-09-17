from inspect import signature


class Dispatcher(dict):
    def __missing__(self, key):
        self[key] = multiple_dispatch_factory()
        return self[key]


def multiple_dispatch_factory():
    def multiple_dispatch(*args, **kwargs):
        generic = None

        for func in multiple_dispatch.funcs:
            sig = signature(func)

            try:
                bound_arguments = sig.bind(*args, **kwargs).arguments
            except TypeError:
                continue

            try:
                ann = func.__annotations__
            except AttributeError:
                generic = func
                continue

            if all(isinstance(bound_arguments[name], type_) for name, type_ in ann.items()):
                return func(*args, **kwargs)

        if generic:
            return generic(*args, **kwargs)

        raise ValueError("No registered function matches the annotation types")
    multiple_dispatch.funcs = []
    return multiple_dispatch


_dispatch_by_name = Dispatcher()
def overloaded(func):
    dispatcher = _dispatch_by_name[func.__name__]
    dispatcher.funcs.append(func)
    return dispatcher


if __name__ == "__main__":
    @overloaded
    def add(x: int, y: int):
        return x + y

    @overloaded
    def add(x: str, y: str):
        return x + y + '!'

    @overloaded
    def add(x: float, y):
        return f'{x} is float, {y} is anything'