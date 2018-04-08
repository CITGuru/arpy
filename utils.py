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
    def __init__(self, command, path, ignorelist, sleeptime, cmd_line, **kwargs):
        super(RestartHandler, self).__init__(**kwargs)
        self.command = command
        self.ignorelist = ignorelist
        self.cmd_line = cmd_line
        self.sleep = sleeptime
        self.start()

    def stop(self):
        try:
            self._process.terminate()
        except:
            pass
        log('red', 'TERMINATED')

    def start(self):
        self._last_restart = time()
        if type(self.command) == list and self.cmd_line:
            for com in self.command:
                try:
                    self._process = Popen(com)
                except Exception as e:
                    log("red", "ERROR in running the command %s. Exception: %s" % (com, e))

                log('green', 'STARTED %s' % self._process)
        else:
            try:
                self._process = Popen(self.command)
            except Exception as e:
                log("red", "ERROR in running the command : %s. Exception: %s" % (self.command, e))
        
        try:
            log('green', 'STARTED %s' % self._process)
        except:
            pass

        
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


def monitor(command, path, action, sleeptime, ignorelist=None, cmd_line=None):
        if action == 'run':
            ev = RestartHandler(command, path=path,
                                sleeptime=sleeptime,
                                ignorelist=ignorelist, cmd_line=cmd_line)
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


