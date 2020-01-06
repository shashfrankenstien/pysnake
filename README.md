# pysnake
Terminal Snake game written in python

![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)

## Installation and Usage

```
$ git clone https://github.com/shashfrankenstien/pysnake.git
$ cd pysnake
$ python -m pip install -r requirements.txt
$ python snake.py
```
<p align="center">
  <img  src="images/snake.png?raw=true">
</p>

```
$ python snake.py --emoji
```

<p align="center">
  <img  src="images/snakeEmoji.png?raw=true">
</p>

## Help

```
$ python snake.py --help
usage: snake.py [-h] [-e] [-c] [-W WIDTH] [-H HEIGHT]

optional arguments:
  -h, --help            show this help message and exit
  -e, --emoji           Use emoji faces 😃
  -c, --nocolor         Don't use colors
  -W WIDTH, --width WIDTH
                        Set frame width in number of characters
  -H HEIGHT, --height HEIGHT
                        Set frame height in number of characters
```