"""Note that Maybe is meant to be used "anonymously".
Assigning Maybe(...) to some variable is asking for trouble as Maybe is singleton.
"""

Null = object()  # Sentinel; None may be a valid attribute value

class MaybeMeta(type):
    """Ensures Maybe is singleton."""
    instance = None

    def __call__(cls, value):
        if MaybeMeta.instance is None:
            MaybeMeta.instance = super(MaybeMeta, cls).__call__()
        setattr(MaybeMeta.instance, f'_{cls.__name__}__value', value)
        return MaybeMeta.instance


class Maybe(metaclass=MaybeMeta):
    def __getattr__(self, attr):
        self.__value = getattr(self.__value, attr, Null)
        return self

    def __or__(self, other):
        if self.__value is Null:
            return other
        return self.__value


if __name__ == "__main__":
    class U: ...
    users = U(); users.bob = U(); users.bob.friends = U(); users.bob.friends.sue = 'sue'
    print(Maybe(users).bob.friends.sue | 'mary')  # attributes all exist, prints 'sue'
    print(Maybe(users).bob.friends.mary | 'peggy')  # mary doesn't exist, prints 'peggy'