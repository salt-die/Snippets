class MaybeMeta(type):
    """This metaclass ensures Maybe(None) is singleton."""
    nothing = None

    def __call__(cls, value):
        if value is None:
            if MaybeMeta.nothing is None:
                MaybeMeta.nothing = super(MaybeMeta, cls).__call__(value)
            return MaybeMeta.nothing

        return super(MaybeMeta, cls).__call__(value)


class Maybe(metaclass=MaybeMeta):
    def __init__(self, value):
        self.__value = value

    def __getattr__(self, attr):
        if self.__value is None:
            return self

        return Maybe(getattr(self.__value, attr, None))

    def __or__(self, other):
        if self.__value is None:
            return other
        return self.__value


if __name__ == "__main__":
    class User:
        def __init__(self, name, friends):
            self.name = name
            self.friends = friends

    class Friends:
        def __init__(self, *friends):
            for friend in friends:
                setattr(self, friend, friend)

    class Users:
        def __init__(self, *users):
            for user in users:
                setattr(self, user.name, user)

    users = Users(User('bob', Friends('sue')))
    print(Maybe(users).bob.friends.sue | 'mary')  # attributes all exist, prints 'sue'
    print(Maybe(users).bob.friends.mary | 'peggy')  # mary doesn't exist, prints 'peggy'