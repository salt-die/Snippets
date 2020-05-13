import ast
import re

NAME_RE = re.compile('[.]([A-Za-z]+)[ ]')
DEFAULT = 3

class IndentProp:
    def __init__(self, indent=DEFAULT):
        self.indent = indent

    @property
    def indent(self):
        return self._indent

    @indent.setter
    def indent(self, value):
        self._indent = value
        self.last = '├' + '─' * (value - 1)
        self.pre = '│' + ' ' * (value - 1)
        self.last_last = '╰' + '─' * (value - 1)
        self.blank = ' ' * value


ind = IndentProp()

def snake(head, tail):
    yield head
    while 1: yield tail

def flatten(iterable):
    for item in iterable:
        if isinstance(item, list):
            yield from item
        else:
            yield item

def stringify(tree):
    if not isinstance(tree, ast.AST):
        yield str(tree)
        return

    leaf_name =  NAME_RE.search(str(tree)).group(1)
    yield leaf_name

    # Put quotes around strings if they're from `value` fields and skip non-`value` fields whose attr is None
    fields = (f"'{attr}'" if isinstance(attr, str) and field == 'value' else attr
              for field in tree._fields if (attr := getattr(tree, field)) is not None or field == 'value')
    fields = tuple(flatten(fields))

    for i, attr in enumerate(fields, start=1):
        head, tail = (ind.last, ind.pre)  if i < len(fields) else (ind.last_last, ind.blank)
        prefix = snake(head, tail)
        yield from (pre + line for pre, line in zip(prefix, stringify(attr)))

def pformat(code, indent=DEFAULT):
    ind.indent = indent
    body = ast.parse(code).body
    return '\n'.join(line for body_part in body for line in stringify(body_part))

def pp(code, indent=DEFAULT): print(pformat(code, indent))
