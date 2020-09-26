Null = object()


class MaybeMeta(type):
    """Cache Maybe(Null)"""
    Nothing = None

    def __call__(cls, val):
        if val is Null:
            if MaybeMeta.Nothing is None:
                MaybeMeta.Nothing = super(MaybeMeta, cls).__call__(val)
            return MaybeMeta.Nothing
        return super(MaybeMeta, cls).__call__(val)


class Maybe(metaclass=MaybeMeta):
    """A class for Chaining attributes that may or may not exist.
    Say we want to assign `x` the value from `users.bob.friends[1].name` if it exists or None if it doesn't:
    `x = Maybe(users).bob.friends[1].name | None`
    """
    def __init__(self, val):
        self.__value = val

    def __getattr__(self, attr):
        return Maybe(getattr(self.__value, attr, Null))

    def __setattr__(self, attr, val):
        if attr == '_Maybe__value':
            return super().__setattr__(attr, val)

        if self.__value is not Null:
            setattr(self.__value, attr, val)

    def __call__(self, *args, **kwargs):
        try:
            return Maybe(self.__value(*args, **kwargs))
        except TypeError:
            return Maybe(Null)

    def __getitem__(self, key):
        try:
            return Maybe(self.__value[key])
        except (TypeError, IndexError, KeyError):
            return Maybe(Null)

    def __or__(self, other):
        if self.__value is Null:
            return other
        return self.__value


if __name__ == '__main__':
    class U: ...
    users = U(); users.bob = U(); sue = U(); sue.name = 'sue'; users.bob.friends = [sue, sue]

    Maybe(users).george.friends.mary = 'mary'  # Does nothing as users.george doesn't exist
    Maybe(users).george | 'No george'  # 'No george'
    Maybe(users).bob.friends[1].birthday = '1/1/00'  # Adds birthday attribute to users.bob.friends[1]
    users.bob.friends[1].birthday  # '1/1/00'
