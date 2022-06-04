from __future__ import annotations
# bouncing text

import argparse
import curses
import random
import time

from typing import Optional
from typing import Sequence


DEFAULT_TEXT = "Text Here"
CURSES_BLACK = 16
SPEED_LIST = [0.01, 0.02, 0.025, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.3]
DEFAULT_SPEED = 5


def color():
    curses.init_pair(2, random.randrange(0, curses.COLORS), CURSES_BLACK)


def curses_main(screen: curses._CursesWindow, args: argparse.Namespace):
    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().
    curses.use_default_colors()
    color()
    screen.bkgd(" ", curses.color_pair(2))
    text = args.text
    speed = args.speed
    x = y = 0
    dx = dy = 1
    text_len = len(text)
    run = True
    while run:
        screen.move(y, 0)
        screen.clrtoeol()
        if x >= curses.COLS - text_len:
            dx = -1
            color()
        elif x == 0:
            dx = 1
            color()
        if y >= curses.LINES - 1:
            dy = -1
            color()
        elif y == 0:
            dy = 1
            color()
        y += dy
        x += dx
        try:
            screen.addstr(y, x, text, curses.color_pair(2))
        except curses.error:
            pass
        screen.refresh()
        ch = screen.getch()
        if ch == curses.KEY_RESIZE:
            curses.update_lines_cols()
            x = min(curses.COLS - text_len, x)
            y = min(curses.LINES - 1, y)
        elif ch in [81, 113]:  # q, Q
            run = False
        elif 48 <= ch <= 57:  # 0 to 9
            speed = int(chr(ch))
        time.sleep(SPEED_LIST[speed])


def positive_int_zero_to_nine(value: str) -> int:
    """
    Used with argparse. Checks to see if value is positive int between 0 and 10.
    """
    msg = f"{value} is an invalid positive int value 0 to 9"
    try:
        int_value = int(value)
        if int_value < 0 or int_value >= 10:
            raise argparse.ArgumentTypeError(msg)
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError(msg)


def argument_parser(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", default=DEFAULT_TEXT, nargs="?",
                        help="Custom text")
    parser.add_argument("-s", "--speed", type=positive_int_zero_to_nine,
                        default=DEFAULT_SPEED,
                        help="Set speed. 0-Fast, 5-Default, 9-Slow")
    return parser.parse_args(argv)


def main():
    args = argument_parser()
    curses.wrapper(curses_main, args)


if __name__ == "__main__":
    main()
