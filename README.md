# x11-key-mapper

## What is it?

x11-key-mapper is a script that re-maps the keys of an input device (keyboard,
foot pedal, etc) to either different keys or to a script, based on the title of
the currently-focused X11 window.

[A fork of `actkbd`](https://github.com/Khouderchah-Alex/actkbd) is used to
trigger configured scripts on keyboard input, while
[`xtitle`](https://github.com/baskerville/xtitle) is used to detect window title
changes. Finally, [`xdotool`](https://github.com/jordansissel/xdotool) is used
to fake new input events.

## How to use it?

`sudo ./setup.sh` should be run first.

Following that, `sudo ./key_mapper.py` is a good starting point, although
configuring this to be run on startup/login could be a better long-term
solution.

Note that any config/*.py file will be interpreted as a configuration
file. As long as all of the config files have a different DEVICE_PATH,
key_mapper will use all of the configs, allowing for multiple devices
to have their keys remapped.
