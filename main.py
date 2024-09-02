import curses
from DataHandler.Handler import DataHandler
import Utils.MenuHandler as m
from Utils.ConfigHandler import ConfigHandler as c
import config
import importlib
import os
from random import randint

def main(stdscr):
    sessionColor = randint(1, 6)
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, sessionColor)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(5, sessionColor, curses.COLOR_BLACK)
    
    menu = [
        "Data -> Video", 
        "Video -> Data", 
        "Download YT Video", 
        "Upload YT Video", 
        "Edit config", 
        "Exit"
    ]
    current_row_idx = 0
    
    m.print_menu(stdscr, current_row_idx, menu)
    
    while True:
        key = stdscr.getch()
        
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu[current_row_idx] == "Exit":
                break
            else:
                if current_row_idx == 0:
                    dataHandler = DataHandler(stdscr) # Inizializzo ogni volta per permettere di ricaricare il config
                    dataHandler.dataToVideo()

                elif current_row_idx == 1:
                    dataHandler = DataHandler(stdscr) # Inizializzo ogni volta per permettere di ricaricare il config
                    dataHandler.videoToData()

                elif current_row_idx == 2:
                    from Utils.YTDownloader.YTHandler import YouTubeVideoDownloader

                    stdscr.clear()
                    m.set_string(stdscr, 0, 0, f"Video ID: \n")
                    curses.echo()
                    vidID = stdscr.getstr(1, 0).decode('utf-8')
                    curses.noecho()

                    YTHandler = YouTubeVideoDownloader()
                    if YTHandler.download_video(vidID):
                        m.set_string(stdscr, 1, 0, f"Downloaded video {vidID}\n", colorCode=2, stop=True)
                    else:
                        m.set_string(stdscr, 1, 0, f"Error in download\n", colorCode=3, stop=True)

                elif current_row_idx == 3:
                    from Utils.YTDownloader.YTHandler import YouTubeVideoDownloader
                    YTHandler = YouTubeVideoDownloader()

                    stdscr.clear()
                    if not os.path.exists(config.video_out):
                        m.set_string(stdscr, 0, 0, f"No video found in dir ({config.video_out})\n", colorCode=3, stop=True)
                        continue

                    m.set_string(stdscr, 0, 0, f"Video title: \n")
                    curses.echo()
                    title = stdscr.getstr(1, 0).decode('utf-8')
                    curses.noecho()

                    m.set_string(stdscr, 1, 0, f"Uploading video {config.video_out} as \"{title}\"\n")
                    m.set_string(stdscr, 2, 0, " ")
                    result = YTHandler.upload_video(config.video_out, title)
                    m.set_string(stdscr, 2, 0, result[0], colorCode=result[1], stop=True)

                elif current_row_idx == 4:
                    configHander = c(stdscr)
                    configHander.edit()
                    importlib.reload(config)                    
        
        m.print_menu(stdscr, current_row_idx, menu)

curses.wrapper(main)
