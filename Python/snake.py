# this porject will uses the curses programming of python, since i work on a mac.
# this involves using syntax related to C-variables.

import curses
from curses import window, wrapper

stdscr = curses.initscr()

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
                win.addch(cood[0], cood[1], ' ')
                cood = (cood[0] - 1, cood[1])
            elif xy == ord('s'):
                win.addch(cood[0], cood[1], ' ')
                cood = (cood[0] + 1, cood[1])   
            elif xy == ord('a'):
                win.addch(cood[0], cood[1], ' ')
                cood = (cood[0], cood[1] - 1)
            elif xy == ord('d'):
                win.addch(cood[0], cood[1], ' ')
                cood = (cood[0], cood[1] + 1)

curses.wrapper(draw_border)