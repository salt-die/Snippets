from dataclasses import is_dataclass, fields

def pretty_print(obj):
    print(nested_stringify(obj))

NESTED_TYPES = dict, list, tuple,  # One can add other containers here along with additional branching in `nested_stringify`

def nested_stringify(obj, indent=4, _indents=0):
    if not isinstance(obj, NESTED_TYPES) and not is_dataclass(obj):
        return stringify(obj)

    next_indent = _leading_spaces(indent, _indents + 1)

    if is_dataclass(obj):
        start, end = type(obj).__name__ + '(', ')'

        middle = '\n'.join(
            f'{next_indent}{field.name}='
            f'{nested_stringify(getattr(obj, field.name), indent, _indents + 1)},' for field in fields(obj)
        )

    elif isinstance(obj, dict):
        start, end = '{}'

        middle = '\n'.join(
            f'{next_indent}{nested_stringify(key, indent, _indents + 1)}: '
            f'{nested_stringify(value, indent, _indents + 2)},' for key, value in obj.items()
        )

    else:
        if isinstance(obj, list):
            start, end = '[]'
        else:  # is tuple
            start, end = '()'

        middle = '\n'.join(
            f'{next_indent}{nested_stringify(item, indent, _indents + 1)},' for item in obj
        )

    return '\n'.join(
        (
            start,
            middle,
            f'{_leading_spaces(indent, _indents)}{end}'
        )
    )

def stringify(obj):
    if isinstance(obj, str):
        return f'"{obj}"'
    return str(obj)

def _leading_spaces(indent, indents):
    return indent * indents * ' '


if __name__ == '__main__':
    from dataclasses import dataclass

    @dataclass
    class Point:
        x: int
        y: int

    @dataclass
    class Coords:
        my_points: list
        my_kwargs: dict

    coords = Coords([Point(1, 2), Point(3, 4)], {"a": 1, "b": 2})

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
    #     my_kwargs={
    #         "a": 1,
    #         "b": 2,
    #     },
    # )