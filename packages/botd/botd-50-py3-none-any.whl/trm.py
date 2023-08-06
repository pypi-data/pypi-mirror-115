# This file is placed in the Public Domain.

import atexit
import importlib
import os
import pkgutil
import sys
import termios

resume = {}

from ob import Bus, Kernel, Handler, kernel


class Runtime(Kernel):

    def error(self, e):
        if type(e) == str:
            cprint(e)
            return
        try:
            cprint(e.txt)
        except:
            try:
                cprint(e.error)
            except:
                try:
                    cprint(e.exc)
                except:
                    pass
        e.ready()


class Client(Handler):

    def __del__(self):
        if self in Bus.objs:
            Bus.objs.remove(self)
 
    def cmd(self, txt):
        k = kernel()
        return k.cmd(self, txt)

    def handle(self, e):
        k = kernel()
        k.put(e)

    def raw(self, txt):
        cprint(txt)

class CLI(Client):

    def handle(self, e):
        k = kernel()
        k.put(e)
        e.wait()

    def error(self, e):
        cprint(str(e))
        e.ready()



class Console(CLI):
    def poll(self):
        return input("> ")


class Test(Handler):
    def handle(self, e):
        k = kernel()
        k.put(e)

    def raw(self, txt):
        k = kernel()
        if k.opts("v"):
            cprint(txt)


def cprint(*args):
    print(*args)
    sys.stdout.flush()


def daemon():
    pid = os.fork()
    if pid != 0:
        termreset()
        os._exit(0)
    os.setsid()
    os.umask(0)
    si = open("/dev/null", "r")
    so = open("/dev/null", "a+")
    se = open("/dev/null", "a+")
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def run(txt):
    c = Client()
    res = c.cmd(txt)
    del c
    return res

def termsetup(fd):
    return termios.tcgetattr(fd)


def termreset():
    if "old" in resume:
        try:
            termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])
        except termios.error:
            pass


def termsave():
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = termsetup(sys.stdin.fileno())
        atexit.register(termreset)
    except termios.error:
        pass


def wrap(func):
    termsave()
    try:
        func()
    except KeyboardInterrupt:
        pass
    except PermissionError as ex:
        cprint(str(ex))
    finally:
        termreset()
