import arpy
# from subprocess import Popen
# auto push to git
arpy.task("push", ["git add .", "git commit -m 'updates'", "git push origin master"], ".", ignorelist=[".git"])


