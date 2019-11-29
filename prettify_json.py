import json

def prettify(file):
    """
    Turn an ugly json into a prettier one.
    """
    with open(file + ".json", "r") as pre_parsed:
        json_to_parse = json.load(pre_parsed)

    parsed = prettyjson(json_to_parse)

    with open(file + "_prettified.json", "w") as rewrite:
        rewrite.write(parsed)

def prettyjson(obj, width=95, scope=0, buffer=0):
    """
    Return obj in a pretty json format.
    """
    if not isinstance(obj, (dict, list, tuple)):
        return stringify(obj)

    joiners = ', ', f',\n{" " * (scope + buffer + 1)}'
    if isinstance(obj, dict):
        for joiner in joiners:
            line = []
            for key, value in obj.items():
                key = stringify(key)
                line.append(f'{key}: {prettyjson(value, width, scope + 1, buffer + len(key) + 2)}')
            line = f'{"{"}{joiner.join(line)}{"}"}'
            if len(line) <= width:
                break
        return line

    for joiner in joiners:
        line = f'[{joiner.join(prettyjson(item, width, scope + 1, buffer) for item in obj)}]'
        if len(line) <= width:
            break
    return line

def stringify(obj):
    if isinstance(obj, str):
        return f'"{obj}"'
    if isinstance(obj, bool):
        return str(obj).lower()
    return str(obj)
