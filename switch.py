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
        _name_to_cases[name] = cases = {}
        funcs_to_vals = {}

        def case(val):
            def deco(func):
                if func in funcs_to_vals:
                    cases[val] = cases[funcs_to_vals[func]].copy()
                else:
                    cases[val] = []
                    funcs_to_vals[func] = val

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
        @case(2)
        def _():
            print(1, 'or', 2)
            yield 20  # yield to break

        @case(3)
        def _():
            print(3)

        @case(4)
        @case('a')
        def _():
            print(4, 'or a')

        @case('default')
        def _():
            print('default')