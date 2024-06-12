#!/bin/python3

import pyautogui
import sys
import re
from dataclasses import dataclass


SUFFIXES = "crhv"
REGEX_NUM = r"^\d{1,3}$"
REGEX_CHAR = r"^\d{{1,3}}[{SUF}]$".format(SUF = SUFFIXES)


@dataclass
class Options:
    click = True
    rows = 12
    columns = 17
    plant_dim = 40
    horizontal = True
    I = 204
    duration = 0.03


def get_opts():
    retval = Options()

    if len(sys.argv) > 1:
        to_be_planted = sys.argv[1]

        if re.match(REGEX_NUM, to_be_planted):
            if 0 < int(to_be_planted) < 204:
                retval.horizontal = True
                retval.I = int(to_be_planted)

        elif re.match(REGEX_CHAR, to_be_planted):

            # Remove suffix
            n = int(to_be_planted.rstrip(SUFFIXES))

            # Make plant intructions
            match to_be_planted[-1]:
                case 'c':
                    retval.horizontal = False
                    if 0 < n <= retval.columns:
                        retval.I = n*retval.rows
                case 'r':
                    retval.horizontal = True
                    if 0 < n <= retval.rows:
                        retval.I = n*retval.columns
                case 'h':
                    retval.horizontal = True
                    if 0 < n <= retval.columns*retval.rows:
                        retval.I = n
                case 'v':
                    retval.horizontal = False
                    if 0 < n <= retval.columns*retval.rows:
                        retval.I = n
                case _:
                    retval = None
        else:
            retval = None

        # Get duration if passed
        if len(sys.argv) == 3:
            try:
                retval.duration = float(sys.argv[2])
            except ValueError:
                retval = None

    return retval


def plant_field(opts):
    if opts is None:
        return
    
    pyautogui.PAUSE = opts.duration
    startX,startY = pyautogui.position()

    # Choose different resposition functions for vertical and horizontal movement
    reposition = (
        lambda d: pyautogui.moveTo(startX, startY+opts.plant_dim*d, pyautogui.PAUSE) 
        if opts.horizontal else 
        pyautogui.moveTo(startX + opts.plant_dim*d, startY, pyautogui.PAUSE)
    )

    # Choose different advance functions for vertical and horizontal movement
    advance = ( 
        lambda : pyautogui.move(opts.plant_dim, 0, pyautogui.PAUSE) 
        if opts.horizontal else 
        pyautogui.move(0, opts.plant_dim, pyautogui.PAUSE)
    )

    outer,inner = (opts.rows, opts.columns) if opts.horizontal else (opts.columns, opts.rows)

    i = 0
    broken = False

    for y in range(outer):
        if broken:
            break

        reposition(y)
        for x in range(inner):
            broken = (i==opts.I)
            if broken:
                break
            if opts.click:
                pyautogui.click()
            i += 1
            advance()


def main():
    opts = get_opts()

    if opts is None:
        print("Error parsing options")
        exit()

    plant_field(opts)


if __name__ == "__main__":
    main()
