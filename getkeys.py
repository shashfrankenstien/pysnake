#!/usr/bin/env python
import sys
import termios
import contextlib
from sys import platform
import msvcrt
# from getch import getch

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
    # print ('exit with ^C or ^D')
    if platform == "win32":
        return msvcrt.getch()
    else:
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
        print (ch)