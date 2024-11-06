#!/bin/python3

import pyautogui
import sys
import re
from dataclasses import dataclass
import configparser
import os


SUFFIXES = "crhv"
REGEX_NUM = r"^\d{1,3}$"
REGEX_CHAR = r"^\d{{1,3}}[{SUF}]$".format(SUF = SUFFIXES)

config_file = "config.ini"
default_section = "DEFAULT"


@dataclass
class Options:
    click: bool = True
    rows: int = 12
    columns: int = 17
    plant_dim: int = 40
    horizontal: bool = True
    duration: float = 0.1

    def __post_init__(self):
        self.I = self.rows * self.columns

    def __str__(self):
        return str(self.__dict__)


def error_msg_helper(what, err, appendix=None):
    retval = f"Error {what}: {err}"
    if appendix:
        retval = f"{retval}\n{appendix}"
    return retval


def create_config_file(path):
    print(f"Creating initial config file \'{path}\'")
    initial_opts = Options()
    config = configparser.ConfigParser()

    config[default_section] = {
        "click": str(initial_opts.click),
        "rows": str(initial_opts.rows),
        "columns": str(initial_opts.columns),
        "plant_dim": str(initial_opts.plant_dim),
        "duration": str(initial_opts.duration),
    }

    with open(path, "w") as file:
        config.write(file)


def get_config_file_path():
    config_dir = os.path.join(
        os.environ.get("APPDATA") or
        os.environ.get("XDG_CONFIG_HOME") or
        os.path.join( os.environ["HOME"], ".config" ), "Wurzelbot"
    )

    try:
        if not os.path.exists(config_dir):
            print(f"Creating missing directory {config_dir}")
            os.makedirs(config_dir)
    except Exception as e:
        print( error_msg_helper("creating config dir", e) )
        config_dir = "."

    return os.path.abspath( os.path.join(config_dir, config_file) )


def load_opts_from_file():
    retval = Options()
    config_file_abs = get_config_file_path()

    # Create config file if it doesn't exist
    try:
        if not os.path.isfile(config_file_abs):
            create_config_file(config_file_abs)
    except Exception as e:
        print( error_msg_helper("creating new config file", e) )

    # Parse config file, result to default values if error occurs
    try:
        config = configparser.ConfigParser()
        config.read(config_file_abs)
        section = config[default_section]
        retval.click = section.getboolean("click", fallback=retval.click)
        retval.rows = section.getint("rows", fallback=retval.rows, raw=False)
        retval.columns = section.getint("columns", fallback=retval.columns)
        retval.I = retval.rows * retval.columns
        retval.plant_dim = section.getint("plant_dim", fallback=retval.plant_dim)
        retval.duration = section.getfloat("duration", fallback=retval.duration)
    except ValueError as e:
        print(error_msg_helper("parsing config file", e, "Using default config"))
        retval = Options()

    return retval


def get_opts():
    retval = load_opts_from_file()

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
    try:
        main()
    except KeyboardInterrupt:
        pass
