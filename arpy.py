from argparse import ArgumentParser, REMAINDER
import sys
from utils import monitor, log

def task(name, command, path, sleeptime=2, ignorelist=None, watchlist="*"):
    log("blue", "starting {} ...".format(name))
    monitor(command, path=path, action="run", sleeptime=2, ignorelist=ignorelist)
    log("blue", "task {} ran".format(name))
    

def watch():
    pass

if __name__ == '__main__':
    
    parser = ArgumentParser(description='''
    Allows to start a program, and to monitor changes in a folder, when changes are
    detected in the folder, the command is restarted.

    This can be useful to test a software you are developping and having immediate
    feedback.
    ''')
    parser.add_argument('-p', '--path', type=str, default='.',
                        help='set the path to monitor for changes')

    parser.add_argument('-a', '--action', type=str, default='run',
                    help='what action to perform when changes are detected')        

    parser.add_argument('-i', '--ignorelist', type=str, default='', nargs='*',
                        help='files to ignore')
                        
    parser.add_argument('-s', '--sleep', type=int, default=0,
                        help='ignore events for n seconds after the last restart')
    parser.add_argument('command', type=str, nargs=REMAINDER)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    log('blue', str(args))
    monitor(args.command, args.path, args.action, args.sleep,
            args.ignorelist, cmd_line=True)
