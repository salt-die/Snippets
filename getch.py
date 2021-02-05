import sys
from io import BytesIO


if sys.platform.startswith('linux'):
    import fcntl
    import os
    import termios
    import tty

    def getch(block=True):
        fd = sys.stdin.fileno()
        settings = termios.tcgetattr(fd)
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)

        try:
            tty.setraw(fd)
            if not block:
                fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
            return sys.stdin.buffer.read(1)
        finally:
            fcntl.fcntl(fd, fcntl.F_SETFL, flags)
            termios.tcsetattr(fd, termios.TCSADRAIN, settings)

elif sys.platform == 'win32':
    import msvcrt

    def getch(block=True):
        if not block and not msvcrt.kbhit():
            return b''
        return msvcrt.getch()

else:
    try:  # Try for Mac
        import Carbon
        Carbon.Evt  # Not in *nix
    except (ModuleNotFoundError, AttributeError) as e:
        raise OSError(f'getch not implemented for {sys.platform}') from e

    def getch(block=True):  # I haven't tested this.
        if not block and Carbon.Evt.EventAvail(0x0008)[0] == 0:  # 0x0008 is the keyDownMask
            return b''
        return bytes(chr(Carbon.Evt.GetNextEvent(0x0008)[1][1] & 0x000000FF), 'utf8')

def flush():
    with BytesIO() as r:
        while c := getch(block=False):
            r.write(c)
        return r.getvalue()
