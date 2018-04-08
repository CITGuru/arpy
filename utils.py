#!/usr/bin/env python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileMovedEvent
from subprocess import Popen, PIPE
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
        if isinstance(self.command, list):
            for com in self.command:
                self._process = Popen(com)
                log('green', 'STARTED %s' % self._process)
        else:
            self._process = Popen(self.command)
            log('green', 'STARTED %s' % self._process)

        
    def on_any_event(self, event):
        if self.sleep and time() < self._last_restart + self.sleep:
            return
        
        if self.ignorelist:
            for i in self.ignorelist:
                r = re.compile('^' + i.replace('*', '.*') + '$')
                if r.match(event.src_path):
                    return
                if isinstance(event, FileMovedEvent) and r.match(event.dest_path):
                    return

        log('blue', '%s RESTARTING' % event)

        self.stop()
        self.start()


def monitor(command, path, action="restart", sleeptime, ignorelist=None):
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


