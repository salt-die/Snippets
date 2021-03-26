from collections.abc import Mapping, Iterable
from dataclasses import is_dataclass, fields

def pretty_print(obj, indent=4):
    """
    Pretty prints a (possibly deeply-nested) dataclass.
    Each new block will be indented by `indent` spaces (default is 4).
    """
    print(stringify(obj, indent))

def stringify(obj, indent=4, _indents=0):
    if isinstance(obj, str):
        return f"'{obj}'"

    if not is_dataclass(obj) and not isinstance(obj, (Mapping, Iterable)):
        return str(obj)

    this_indent = indent * _indents * ' '
    next_indent = indent * (_indents + 1) * ' '
    start, end = f'{type(obj).__name__}(', ')'  # generic start and end -- dicts, lists, and tuples will re-assign this

    if is_dataclass(obj):
        body = '\n'.join(
            f'{next_indent}{field.name}='
            f'{stringify(getattr(obj, field.name), indent, _indents + 1)},' for field in fields(obj)
        )

    elif isinstance(obj, Mapping):
        if isinstance(obj, dict):
            start, end = '{}'

        body = '\n'.join(
            f'{next_indent}{stringify(key, indent, _indents + 1)}: '
            f'{stringify(value, indent, _indents + 1)},' for key, value in obj.items()
        )

    else:  # is Iterable
        if isinstance(obj, list):
            start, end = '[]'
        elif isinstance(obj, tuple):
            start = '('

        body = '\n'.join(
            f'{next_indent}{stringify(item, indent, _indents + 1)},' for item in obj
        )

    return f'{start}\n{body}\n{this_indent}{end}'

if __name__ == '__main__':
    from dataclasses import dataclass

    @dataclass
    class Point:
        x: int
        y: int

    @dataclass
    class Coords:
        my_points: list
        my_dict: dict

    coords = Coords([Point(1, 2), Point(3, 4)], {'a': (1, 2), (1, 2): 'a'})

    pretty_print(coords)

    # Coords(
    #     my_points=[
    #         Point(
    #             x=1,
    #             y=2,
    #         ),
    #         Point(
    #             x=3,
    #             y=4,
    #         ),
    #     ],
    #     my_dict={
    #         'a': (
    #             1,
    #             2,
    #         ),
    #         (
    #             1,
    #             2,
    #         ): 'a',
    #     },
    # )
