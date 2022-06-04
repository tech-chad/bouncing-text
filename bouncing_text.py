from __future__ import annotations
# bouncing text

import curses
import random
import time


DEFAULT_TEXT = "Text Here"
CURSES_BLACK = 16


def color():
    curses.init_pair(2, random.randrange(0, curses.COLORS), CURSES_BLACK)


def curses_main(screen: curses._CursesWindow):
    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().
    curses.use_default_colors()
    color()
    screen.bkgd(" ", curses.color_pair(2))
    text = DEFAULT_TEXT
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
        time.sleep(0.08)


def main():
    curses.wrapper(curses_main)


if __name__ == "__main__":
    main()
