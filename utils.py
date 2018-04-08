#!/usr/bin/env python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileMovedEvent
from subprocess import Popen, PIPE
from argparse import ArgumentParser, REMAINDER
from time import time, sleep
import re
import six

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

parser = ArgumentParser(description='''
Allows to start a program, and to monitor changes in a folder, when changes are
detected in the folder, the command is restarted.

This can be useful to test a software you are developping and having immediate
feedback.
Or to restart a daemon when configuration or data changes.
Or any other use, the sky is the limit :)
''')
parser.add_argument('-p', '--path', type=str, default='.',
                    help='set the path to monitor for changes')
parser.add_argument('-a', '--action', type=str, default='restart',
                    help='what action to perform when changes are detected')
parser.add_argument('-i', '--ignorelist', type=str, default='', nargs='*',
                    help='files to ignore')
parser.add_argument('-s', '--sleep', type=int, default=0,
                    help='ignore events for n seconds after the last restart')
parser.add_argument('command', type=str, nargs=REMAINDER)


def log(color, string):
    if colored:
        six.print_(colored(string, color))
    else:
        six.print_(string)


class RestartHandler(FileSystemEventHandler):
    def __init__(self, command, path, ignorelist, sleeptime, **kwargs):
        super(RestartHandler, self).__init__(**kwargs)
        self.command = command
        self.ignorelist = ignorelist
        self.sleep = sleeptime
        self.start()

    def stop(self):
        self._process.terminate()
        log('red', 'TERMINATED')

    def start(self):
        self._last_restart = time()
        
        self._process = Popen(self.command)
        log('green', 'STARTED %s' % self._process)

        
    def on_any_event(self, event):
        if self.sleep and time() < self._last_restart + self.sleep:
            return

        for i in self.ignorelist:
            r = re.compile('^' + i.replace('*', '.*') + '$')
            if r.match(event.src_path):
                return
            if isinstance(event, FileMovedEvent) and r.match(event.dest_path):
                return

        log('blue', '%s RESTARTING' % event)

        self.stop()
        self.start()


def monitor(command, path, action, sleeptime, ignorelist=None):
        if action == 'restart':
            ev = RestartHandler(command, path=path,
                                sleeptime=sleeptime,
                                ignorelist=ignorelist)
        else:
            raise NotImplementedError('action %s not implemented' % action)

        ob = Observer()
        ob.schedule(ev, path=path, recursive=True)
        ob.start()
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            ob.stop()
        ob.join()

if __name__ == '__main__':
    args = parser.parse_args()
    log('blue', str(args))
    monitor(args.command, args.path, args.action, args.sleep,
            args.ignorelist)
