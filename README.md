# Arpy - Auto Reload Python

This is a simple tool that helps you automatically run task whenever there is an event in path specified. For instance, if you want to see an immediate results whenever you are developing, you can easily use this to run a command whenever you save the file. Influence by Gulp. Gulp is my favorite build system tooling

# Installation

Its currently in development stage, but you can still try it out.

1. Clone this repo - https://github.com/CITGuru/arpy.git
2. Head into the arpy directory and do `pip install -r requirements.txt`
3. Then add the arpy core files into the path you are importing it. `arpy.py` and `utils.py`


# Usage

## In python scripts
```
import arpy
arpy.task(
    "push", ["git add .", "git commit -m 'updates'", "git push origin master"], ".", ignorelist=[".git"]
)
```
## In command line 

### Usage 

In case you want to use its command line features, add the arpy directory to your system path.

``` arpy.py [-h] [-p PATH] [-a ACTION] [-f SECONDS] [-i IGNORELIST] [-s SECONDS] command```

You can do

```aryp.py -p path/to/dir -s 2 -a run git add .```



# Contribution

Its open source, you can contribute on it. You can contact me here: http://facebook.com/oyetoke.tobi

# Todo
1. Ability to run python functions 
2. Abilty to set event e.g arpy.task("push", command="git push", path=".", on="save")
3. Add watch capability

# Author

Oyetoke Toby - A C#, Python, Javascript, Kivy lover.