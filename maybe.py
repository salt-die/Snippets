Null = object()  # Sentinel, None may be a valid attribute value

class MaybeMeta(type):
    """This metaclass ensures Maybe(Null) is singleton."""
    nothing = None

    def __call__(cls, value):
        if value is Null:
            if MaybeMeta.nothing is None:
                MaybeMeta.nothing = super(MaybeMeta, cls).__call__(value)
            return MaybeMeta.nothing

        return super(MaybeMeta, cls).__call__(value)


class Maybe(metaclass=MaybeMeta):
    def __init__(self, value):
        self.__value = value

    def __getattr__(self, attr):
        if self.__value is Null:
            return self

        return Maybe(getattr(self.__value, attr, Null))

    def __or__(self, other):
        if self.__value is Null:
            return other
        return self.__value


if __name__ == "__main__":
    class U: ...
    users = U(); users.bob = U(); users.bob.friends = U(); users.bob.friends.sue = 'sue'
    print(Maybe(users).bob.friends.sue | 'mary')  # attributes all exist, prints 'sue'
    print(Maybe(users).bob.friends.mary | 'peggy')  # mary doesn't exist, prints 'peggy'