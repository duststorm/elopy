#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Use elo touchscreen as mouse input

Copyright 2015 Jonas Hauquier
Distributed under the terms of the GNU General Public License (GPL version 3 or any later version).
"""

from pymouse import PyMouse
import main as elomain

LMB = 1
RMB = 3

def main():
    mouse = PyMouse()

    def move_mouse(pos):
        x,y = pos
        mouse.move(x,y)
        mouse.click(x,y, LMB)

    elomain.main(callback=move_mouse)


if __name__ == '__main__':
    main()
