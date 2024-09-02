import curses

def print_menu(stdscr, selected_row_idx, menu):
    stdscr.clear()
    banner(stdscr)
    h, w = stdscr.getmaxyx()
    
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()

def set_string(stdscr, y, x, text, stop = False, colorCode = False, clear=True):
    if clear:
        stdscr.move(y,x)
        stdscr.clrtoeol()

    if colorCode:
        stdscr.attron(curses.color_pair(colorCode))
        stdscr.addstr(y, x, text)
        stdscr.attroff(curses.color_pair(colorCode))
    else:
        stdscr.addstr(y, x, text)

    stdscr.refresh()

    if stop:
        stdscr.getch()

def banner(stdscr):
    bannerText = ['┓┏┏┓┓     ┓',
'┗┫┃ ┃┏┓┓┏┏┫',
'┗┛┗┛┗┗┛┗┻┗┻']
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(bannerText):
        x = w//2 - len(row)//2
        stdscr.attron(curses.color_pair(5))
        stdscr.addstr(idx+1, x, row)

    stdscr.attroff(curses.color_pair(5))


           
