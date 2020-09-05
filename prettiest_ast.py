import ast
import re

NAME_RE = re.compile('[.]([A-Za-z]+)[ ]')
DEFAULT = 3
LINE_CHRS = '├─', '│ ', '╰─', '  '

def flatten(iterable):
    for item in iterable:
        if isinstance(item, list):
            yield from item
        else:
            yield item

def snake(head, tail):
    yield head
    while 1: yield tail
    
def prefixes(nfields, indent):
    head, tail, last_head, last_tail = (a + b * (indent - 1) for a, b in LINE_CHRS)
    for _ in range(nfields - 1):
        yield snake(head, tail)
    yield snake(last_head, last_tail)

def stringify(tree, indent):
    if not isinstance(tree, ast.AST):
        yield str(tree)
        return

    leaf_name = NAME_RE.search(str(tree)).group(1)
    yield leaf_name

    # Put quotes around strings if they're from `value` fields and skip non-`value` fields whose attr is None
    fields = (f"'{attr}'" if isinstance(attr, str) and field == 'value' else attr
              for field in tree._fields if (attr := getattr(tree, field)) is not None or field == 'value')
    fields = tuple(flatten(fields))

    for prefix, attr in zip(prefixes(len(fields), indent), fields):
        yield from (pre + line for pre, line in zip(prefix, stringify(attr, indent)))

def pformat(code, indent=DEFAULT):
    body = ast.parse(code).body
    return '\n'.join(line for body_part in body for line in stringify(body_part, indent))

def pp(code, indent=DEFAULT): print(pformat(code, indent))
