import arpy

arpy.task(
    "push", ["git add .", "git commit -m 'updates'", "git push origin master"], ".", ignorelist=[".git"]
)