# this porject will uses the curses programming of python, since i work on a mac.
# this involves using syntax related to C-variables.

import curses
from curses import window, wrapper

stdscr = curses.initscr()

def check_coords(new_y, new_x):
    if new_y < 1 or new_y > 18 or new_x < 1 or new_x > 98:
        return False
    return True

def draw_border(stdscr):
        win = curses.newwin(20, 100, 2, 4)
        win.border(0, 0, 0, 0, 0, 0, 0, 0) 
        cood = (9, 49)
        while True:
            win.addch(cood[0], cood[1], '■')
            win.refresh()
            xy = win.getch()
            if xy not in [ord('w'), ord('s'), ord('a'), ord('d'), ord('q')]:
                pass
            elif xy == ord('q'):
                break
            elif xy == ord('w'):
                new_coords = (cood[0] - 1, cood[1])
                if check_coords(new_coords[0], new_coords[1]):
                    win.addch(cood[0], cood[1], ' ')
                    cood = new_coords
            elif xy == ord('s'):
                new_coords = (cood[0] + 1, cood[1])
                if check_coords(new_coords[0], new_coords[1]):
                    win.addch(cood[0], cood[1], ' ')
                    cood = new_coords   
            elif xy == ord('a'):
                new_coords = (cood[0], cood[1] - 1)
                if check_coords(new_coords[0], new_coords[1]):
                    win.addch(cood[0], cood[1], ' ')
                    cood = new_coords
            elif xy == ord('d'):
                new_coords = (cood[0], cood[1] + 1)
                if check_coords(new_coords[0], new_coords[1]):
                    win.addch(cood[0], cood[1], ' ')
                    cood = new_coords

curses.wrapper(draw_border)