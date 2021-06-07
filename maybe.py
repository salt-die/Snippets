class Maybe:
    """
    A class for Chaining attributes that may or may not exist.
    Say we want to assign `x` the value from `users.bob.friends[1].name` if it exists or None if it doesn't:
    `x = Maybe(users).bob.friends[1].name | None`
    """
    def __init__(self, val):
        object.__setattr__(self, '_Maybe__value', val)

    def __getattr__(self, attr):
        try:
            return Maybe(getattr(self.__value, attr))
        except AttributeError:
            return NOPE

    def __setattr__(self, attr, val):
        if self is not NOPE:
            setattr(self.__value, attr, val)

    def __call__(self, *args, **kwargs):
        try:
            return Maybe(self.__value(*args, **kwargs))
        except TypeError:
            return NOPE

    def __getitem__(self, key):
        try:
            return Maybe(self.__value[key])
        except (TypeError, IndexError, KeyError):
            return NOPE

    def __or__(self, other):
        if self is NOPE:
            return other
        return self.__value


NOPE = Maybe(object())

if __name__ == '__main__':
    class U: ...
    users = U(); users.bob = U(); sue = U(); sue.name = 'sue'; users.bob.friends = [sue, sue]

    Maybe(users).george.friends.mary = 'mary'  # Does nothing as users.george doesn't exist
    Maybe(users).george | 'No george'  # 'No george'
    Maybe(users).bob.friends[1].birthday = '1/1/00'  # Adds birthday attribute to users.bob.friends[1]
    users.bob.friends[1].birthday  # '1/1/00'
