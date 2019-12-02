import json

def prettify(file):
    """
    Turn an ugly json into a prettier one.

    '.json' is left off of file for m̶y̶  your convenience.
    """
    with open(f'{file}.json', "r") as ugly, open(f'{file}_prettified.json', "w") as pretty:
        pretty.write(prettyjson(json.load(ugly)))

def prettyjson(obj, width=95, buffer=0):
    """
    Return obj in a pretty json format.
    """
    if not isinstance(obj, (dict, list, tuple)):
        return stringify(obj)

    if isinstance(obj, dict):
        open_, close, line = *'{}', []
        for key, value in obj.items():
            key = stringify(key)
            line.append(f'{key}: {prettyjson(value, width, buffer + len(key) + 3)}')
    else:
        open_, close, line = *'[]', [prettyjson(item, width, buffer + 1) for item in obj]

    joiners = ', ', f',\n{" " * (buffer + 1)}'
    for joiner in joiners:
        joined = f'{open_}{joiner.join(line)}{close}'
        if len(joined) <= width:
            break
    return joined

def stringify(obj):
    if isinstance(obj, str):
        return f'"{obj}"'
    if isinstance(obj, bool):
        return str(obj).lower()
    return str(obj)
