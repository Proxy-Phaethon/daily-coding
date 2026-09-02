# this project will uses the curses programming of python, since i work on a mac.
# this involves using syntax related to C-variables.

import curses
from curses import window, wrapper
import random

stdscr = curses.initscr()

def check_coords(new_y, new_x):
    if new_y < 1 or new_y > 18 or new_x < 1 or new_x > 98:
        return False
    return True

def draw_border(stdscr):
        win = curses.newwin(20, 100, 2, 4)
        win.border(0, 0, 0, 0, 0, 0, 0, 0) 
        curses.start_color()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        cood = [(9, 49)]
        food = (food_y, food_x) = (random.randint(1, 18), random.randint(1, 98))
        while True:
            win.addch(cood[0][0], cood[0][1], '■', curses.color_pair(1))
            win.addch(food_y, food_x, '●', curses.color_pair(2))
            win.refresh()
            xy = win.getch()

            new_head = None

            if xy == ord('q'):
                break
            elif xy == ord('w'):
                new_head = (cood[0][0] - 1, cood[0][1])
            elif xy == ord('s'):
                new_head = (cood[0][0] + 1, cood[0][1])
            elif xy == ord('a'):
                new_head = (cood[0][0], cood[0][1] - 1)
            elif xy == ord('d'):
                new_head = (cood[0][0], cood[0][1] + 1)

            if new_head is not None and check_coords(new_head[0], new_head[1]):
                if new_head == food:
                    cood.insert(0, new_head)
                    food = (food_y, food_x) = (random.randint(1, 18), random.randint(1, 98))
                else:
                    tail = cood[-1]
                    cood.insert(0, new_head)
                    cood.pop()
                    win.addch(tail[0], tail[1], ' ', curses.color_pair(0))

curses.wrapper(draw_border) 