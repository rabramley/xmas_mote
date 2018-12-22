#!/usr/bin/env python

import time
import itertools
import random
from colorsys import hsv_to_rgb

from mote import Mote


mote = Mote()

num_pixels = 16

mote.configure_channel(1, num_pixels, False)
mote.configure_channel(2, num_pixels, False)
mote.configure_channel(3, num_pixels, False)
mote.configure_channel(4, num_pixels, False)

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 150, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 150)
MAGENTA = (150, 0, 150)

shades = [
    RED,
    YELLOW,
    GREEN,
    CYAN,
    BLUE,
    MAGENTA,
]


def random_shades():
    s = shades[:]
    random.shuffle(s)
    return s

def set_column(col, shade):
    for p in range(mote.get_pixel_count(col)):
        mote.set_pixel(col, p, *shade)


def set_row(row, shade):
    for col in range(1, 5):
        mote.set_pixel(col, row, *shade)


def pause_reducing():
    for pause in [x / 20 for x in range(20, 1, -1)]:
        for _ in range(int(2 / pause)):
            yield
            time.sleep(pause)


def animate_halves():

    _randoms = random_shades()[:2]
    _randoms.extend(reversed(_randoms))

    _shades = itertools.cycle(itertools.chain(*[
        itertools.repeat(s, 2) for s in _randoms
    ]))

    for _ in pause_reducing():

        for column in range(1, 5):
            set_column(column, next(_shades))

        mote.show()


def animate_columns():

    _shades = itertools.cycle(random_shades())

    s = []

    for _ in range(1, 5):
       s.insert(0, next(_shades))

    for _ in pause_reducing():

        for column in range(1, 5):
            set_column(column, s[column - 1])

        s.pop()
        s.insert(0, next(_shades))
        mote.show()


def animate_rows():

    _shades = itertools.cycle(itertools.chain(*[
        itertools.repeat(s, 4) for s in random_shades()
    ]))

    for _ in pause_reducing():

        for row in range(num_pixels - 1, 0, -1):
            old_shade = mote.get_pixel(1, row - 1)
            set_row(row, old_shade)

        set_row(0, next(_shades))
        mote.show()

try:

    animations = [
        animate_rows,
        #animate_columns,
        #animate_halves,
    ]

    while True:
        random.choice(animations)()

except KeyboardInterrupt:
    pass

mote.clear()
mote.show()
time.sleep(0.1)
