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
            ch = sys.stdin.buffer.read(1)
        finally:
            fcntl.fcntl(fd, fcntl.F_SETFL, flags)
            termios.tcsetattr(fd, termios.TCSADRAIN, settings)

        return ch

elif sys.platform == 'win32':
    import msvcrt

    def getch(block=True):
        if not block and not msvcrt.kbhit():
            return b''
        return msvcrt.getch()

else:
    raise OSError(f'getch not implemented for {sys.platform}')

def flush():
    with BytesIO() as r:
        while c := getch(block=False):
            r.write(c)
        return r.getvalue()
