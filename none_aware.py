from inspect import currentframe, getframeinfo

def maybe(val):
    """`x = maybe(val)` is roughly equivalent to `x = val if val is not None else x`
    When assigning to some variable, say `x`, maybe(val) will return val if val is not None else will return x.

    Warning:: Variable must exist prior to this assignment.  Will raise error if not used in an assignment or if
    some name or attribute on the lhs of the assignment isn't defined.
    """
    if other is not None:
        return val if val is not None else other

    parent_frame = currentframe().f_back
    line = getframeinfo(parent_frame).code_context[0]
    var, sep, _ = line.partition('=')

    if not sep:
        raise SyntaxError('maybe(val) needs to be called in an assignment expression')

    glob = parent_frame.f_locals
    loc = {}
    exec(f'val = {var}', glob, loc)

    return val if val is not None else loc['val']
