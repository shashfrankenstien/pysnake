#!/usr/bin/env python
import sys

import contextlib
from sys import platform

if platform == "win32":
    import msvcrt

    class keys:
        UP = [b'\xe0', b'H']
        DOWN = [b'\xe0', b'P']
        RIGHT = [b'\xe0', b'M']
        LEFT = [b'\xe0', b'K']
        W = b'W'
        S = b'S'
        A = b'A'
        D = b'D'
        Q = b'Q'

    def getch():
        out = []
        while True:
            ch = msvcrt.getch()
            out.append(ch)
            if not ch==b'\xe0':
                if len(out)==1:
                    return out[0]
                else:
                    return out
                out = []

else:
    import termios
# from getch import getch

    class keys:
        UP = [27, 91, 65]
        DOWN = [27, 91, 66]
        RIGHT = [27, 91, 67]
        LEFT = [27, 91, 68]
        W = ([87] or [119])
        S = ([83] or [115])
        A = ([65] or [97])
        D = ([68] or [100])
        Q = ([81] or [113])

    @contextlib.contextmanager
    def raw_mode(file):
        old_attrs = termios.tcgetattr(file.fileno())
        new_attrs = old_attrs[:]
        new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
        try:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
            yield
        finally:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)


    def getch():
    # print ('exit with ^C or ^D)
        wait = False
        with raw_mode(sys.stdin):
            try:
                out = []
                while True:
                    ch = sys.stdin.read(1)
                    if not ch or ch == chr(4):
                        break
                    if ord(ch)==27:
                        wait = True
                    if not wait:
                        return [ord(ch)]
                    else:
                        out.append(ord(ch))
                        if ord(ch)==27 or ord(ch)==91:
                            wait=True 
                        else:
                            return out
                    # print (ord(ch))
            except (KeyboardInterrupt, EOFError) as e:
                print(e)

def do_getch():
    while True:
        x = getch()
        if not x: break
        yield x

if __name__ == '__main__':
    for ch in do_getch():
        if ch==keys.UP:
            print('up')
        else:
            print(ch)