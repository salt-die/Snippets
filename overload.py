from inspect import signature


class dynamicdict(dict):
    def __init__(self, default_factory, **kwargs):
        super().__init__(**kwargs)
        self._default_factory = default_factory

    def __missing__(self, key):
        self[key] = self._default_factory(key)
        return self[key]


class FuncStorage:
    def __init__(self, name):
        self.name = name
        self.funcs = []

    def __call__(self, *args, **kwargs):
        generic = None  # If arguments bind to a function with no annotation we'll remember and move on
        for func in self.funcs:
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

    def __repr__(self):
        return f'overloaded function {self.name}'


_func_storage_by_name = dynamicdict(FuncStorage)
def overloaded(func):
    func_storage = _func_storage_by_name[func.__name__]
    func_storage.funcs.append(func)
    return func_storage


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