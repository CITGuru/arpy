import os
import sys
from subprocess import Popen, PIPE
from argparse import ArgumentParser, REMAINDER
from time import time, sleep
import re
import six
from utils import RestartHandler, monitor


try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None


def log(color, string):
    if colored:
        six.print_(colored(string, color))
    else:
        six.print_(string)


def task(name, command, path, sleeptime=2, ignorelist=None, watchlist="*"):
    log("blue", "starting {} ...".format(name))
    monitor(command, path=path, action="restart", sleeptime=2, ignorelist=None)
    
    pass


task("sass", "git add . && git commit -m \"updates\"", ".", sleeptime=2)