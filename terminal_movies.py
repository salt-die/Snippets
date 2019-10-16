"""
Watch movies in your terminal with this handy video-to-ascii converter.

Play movie like so:
>>>python3 terminal_movies.py path/to/movie
"""

import cv2
import curses
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to movie")
args = parser.parse_args()
path = args.path

ascii_map = dict(enumerate(' .,:;<+*LtCa4U80dQM@'))
scale = 255/len(ascii_map) + .05  #Add a small amount to prevent key errors

def main(screen):
    init_curses(screen)
    movie = cv2.VideoCapture(path)
    running = read_flag = True
    while read_flag and running:
        screen_height, screen_width = screen.getmaxyx()
        read_flag, frame = movie.read()

        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(grayscale, (int(screen_width), int(screen_height)))

        for row_num, row in enumerate(resized):
            screen.addstr(row_num, 0,
                          ''.join(ascii_map[int(color/scale)] for color in row[:-1]))
        screen.refresh()
        running = screen.getch() != ord('q')

    movie.release()

def init_curses(screen):
    curses.noecho()
    curses.cbreak()
    screen.nodelay(1)
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    screen.attron(curses.color_pair(1))
    screen.clear()

if __name__ == '__main__':
    curses.wrapper(main)