# PixelColor

[![Travis CI Build Status](https://img.shields.io/travis/com/muflone/pixelcolor/master.svg)](https://www.travis-ci.com/github/muflone/pixelcolor)
[![CircleCI Build Status](https://img.shields.io/circleci/project/github/muflone/pixelcolor/master.svg)](https://circleci.com/gh/muflone/pixelcolor)
[![PyPI - Version](https://img.shields.io/pypi/v/PixelColor.svg)](https://pypi.org/project/PixelColor/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/PixelColor.svg)](https://pypi.org/project/PixelColor/)

**Description:** Get the screen pixel color

**Copyright:** 2022 Fabio Castelli (Muflone) <muflone@muflone.com>

**License:** GPL-3+

**Source code:** https://github.com/muflone/pixelcolor

**Documentation:** http://www.muflone.com/pixelcolor/

# Description

PixelColor is a command line tool to get the color of a pixel from the screen.

You can simply pass the pixel coordinates (X and Y) and the pixel color will
be printed as result.

# System Requirements

* Python 3.x
* Pillow 9.3.0 (https://pypi.org/project/Pillow/)

# Usage

PixelColor is a command line utility and it requires some arguments to be passed:

```
pixelcolor --x <X> --y <Y> [--display <DISPLAY>] [--triplets] [--hex] [--upper]
```

The arguments `--x` and `--y` refer to the pixel coordinates as left and top
positions (the first pixel is always 1x1).

The argument `--display` is the graphical display to use (the `DISPLAY`
variable).

The argument `--triplets` will return the pixel color value as a triplets of
colors (red, green, blue).

The argument `--hex` will show the colors as hexadecimal values.

The argument `--upper` will return the hexadecimal digits as upper case.

An example to execute PixelColor will be the following:

```
pixelcolor --x 100 --y 200 --hex
```

This will print the pixel color at coordinates 100x200.
