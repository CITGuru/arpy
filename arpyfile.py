import arpy

# auto push to git
arpy.task("git", ["git add .", "git commit -m 'updates'", "git push origin master"], path="path/to/file", ignorelist=[".pyc"])

