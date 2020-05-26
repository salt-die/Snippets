"""Another switch implementation"""
from collections import ChainMap

_name_to_cases = {}
class SwitchMeta(type):
    def __call__(cls, value):
        cases = _name_to_cases[cls.__name__]

        default = cases.get('default', [lambda: None])

        funcs = cases.get(value, default)

        for func in funcs:
            if is_generator := func():
                return next(is_generator)

    def __prepare__(name, *args):
        cases = {}
        _name_to_cases[name] = cases

        def case(val):
            def deco(func):
                cases[val] = []
                for case in cases:
                    cases[case].append(func)
                return func
            return deco

        return ChainMap({}, {'case': case})

    def __new__(meta, name, bases, methods):
        methods = methods.maps[0]
        return super().__new__(meta, name, bases, methods)


class switch(metaclass=SwitchMeta): pass


if __name__ == "__main__":
    class my_switch(switch):
        @case(1)
        def _():
            print(1)
            yield 20  # yield to break

        @case(3)
        def _():
            print(3)

        @case('a')
        def _():
            print('a')

        @case('default')
        def _():
            print('default')