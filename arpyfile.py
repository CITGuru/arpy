import arpy
from subprocess import Popen
# auto push to git
# arpy.task("echo", ["echo ran"], path=".", ignorelist=[".pyc"])

Popen(["echo", "ran", "gate"])
