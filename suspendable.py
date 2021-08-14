class Suspendable:
    """
    An asyncio task that can be suspended.
    """
    def __init__(self, coro):
        self._coro = coro
        self._is_suspended = False
        self._task = asyncio.ensure_future(self)

    @property
    def is_suspended(self):
        return self._is_suspended

    def __await__(self):
        while True:
            if self._is_suspended:
                yield

            else:
                try:
                    yield self._coro.send(None)
                except StopIteration as e:
                    return e.value

    def suspend(self):
        self._is_suspended = True

    def resume(self):
        self._is_suspended = False
