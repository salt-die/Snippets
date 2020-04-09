"""a DefaultDict that accepts single argument lambdas"""

class DynamicDict(dict):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        if key not in self:
            super().__setitem__(key, self.func(key))
        return super().__getitem__(key)