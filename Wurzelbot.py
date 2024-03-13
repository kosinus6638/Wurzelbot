#!/bin/python3

import pyautogui
import sys
import re



SUFFIXES = "crhv"
REGEX_NUM = "^\d{1,3}$"
REGEX_CHAR = "^\d{{1,3}}[{SUF}]$".format(SUF = SUFFIXES)

CLICK = True


class Options:
    rows = 12
    columns = 17
    plant_dim = 40
    horizontal = True
    I = 204
    duration = 0.01


def get_opts():
    global I
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
                    if 0 < n < retval.columns:
                        retval.horizontal = False
                        retval.I = n*retval.rows
                case 'r':
                    if 0 < n < retval.rows:
                        retval.horizontal = True
                        retval.I = n*retval.columns
                case 'h':
                    if 0 < n < retval.columns*retval.rows:
                        retval.horizontal = True
                        retval.I = n
                case 'v':
                    if 0 < n < retval.columns*retval.rows:
                        retval.horizontal = False
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

    if opts.horizontal:
        i = 0
        broken = False

        for y in range(opts.rows):

            if broken:
                break

            pyautogui.moveTo(startX, startY + opts.plant_dim*y, pyautogui.PAUSE)
            for x in range(opts.columns):
                broken = (i==opts.I)
                if broken:
                    break
                if CLICK:
                    pyautogui.click()
                i += 1
                pyautogui.move(opts.plant_dim, 0, pyautogui.PAUSE)
    else:
        i = 0
        broken = False
        
        for y in range(opts.columns):

            if broken:
                break

            pyautogui.moveTo(startX + opts.plant_dim*y, startY, pyautogui.PAUSE)
            for x in range(opts.rows):
                broken = (i==opts.I)
                if broken:
                    break
                if CLICK:
                    pyautogui.click()
                i += 1
                pyautogui.move(0, opts.plant_dim, pyautogui.PAUSE)


def main():
    opts = get_opts()

    if opts is None:
        print("Error parsing options")
        exit()

    print(opts.I)
    print(opts.horizontal)
    print(opts.duration)

    plant_field(opts)


if __name__ == "__main__":
    main()