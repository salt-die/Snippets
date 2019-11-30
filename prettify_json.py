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

    joiners = ', ', f',\n{" " * (buffer + 1)}'
    for joiner in joiners:
        if isinstance(obj, dict):
            line = []
            for key, value in obj.items():
                key = stringify(key)
                line.append(f'{key}: {prettyjson(value, width, buffer + len(key) + 3)}')
            line = f'{"{"}{joiner.join(line)}{"}"}'
        else:
            line = f'[{joiner.join(prettyjson(item, width, buffer + 1) for item in obj)}]'
        if len(line) <= width:
            break
    return line

def stringify(obj):
    if isinstance(obj, str):
        return f'"{obj}"'
    if isinstance(obj, bool):
        return str(obj).lower()
    return str(obj)
