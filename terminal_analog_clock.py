import os
import time
import numpy as np

TERMX, _ = os.get_terminal_size()

one =   [[0,0,0], [0,0,8], [0,0,8]]
two =   [[0,7,0], [0,7,8], [8,7,0]]
three = [[0,7,0], [0,7,8], [0,7,8]]
four =  [[0,0,0], [8,7,8], [0,0,8]]
five =  [[0,7,0], [8,7,0], [0,7,8]]
six =   [[0,7,0], [8,7,0], [8,7,8]]
seven = [[7,7,0], [0,0,8], [0,0,8]]
eight = [[0,7,0], [8,7,8], [8,7,8]]
nine =  [[0,7,0], [8,7,8], [0,0,8]]
zero =  [[0,7,0], [8,0,8], [8,7,8]]
colon = [[0,0,0], [0,6,0], [0,6,0]]

digits = [zero, one, two, three, four, five, six, seven, eight, nine]

def center(*lines):
    for line in lines:
        yield line.center(TERMX)

def format(part):
    return [digits[int(i)] for i in f"0{part}"[-2:]]

def digital_time():
    hours, minutes, seconds = map(format, time.localtime()[3:6])
    return np.array([*zip(*hours, colon, *minutes, colon, *seconds)]).reshape(3, 24)


class Clock:
    RADIUS = 23
    CENTER = np.array((RADIUS, RADIUS))


    def __init__(self):
        self.grid = np.pad(np.zeros((self.RADIUS * 2, ) * 2, dtype=int), pad_width=1,
                           mode='constant', constant_values=1)
        self.draw_face()
        self.base = self.grid.copy()

    def reset(self):
        self.grid = self.base.copy()

    def line_segment(self, angle, start, stop, value):
        """
        Draw a line segment.

        start, stop are between 0-1 and represent percentage of RADIUS
        """
        start = start * self.RADIUS
        stop = stop * self.RADIUS

        angle -= np.pi / 2
        angle = np.array([np.sin(angle), np.cos(angle)])
        with np.errstate(divide="ignore"):
            delta = abs(1 / angle)
        step = 2 * np.heaviside(angle, 1) - 1
        side_dis = ((step + 1) / 2) * delta
        map_pos = self.CENTER.copy()

        while True:
            side = 0 if side_dis[0] < side_dis[1] else 1
            side_dis[side] += delta[side]
            map_pos[side] += step[side]
            length = np.linalg.norm(map_pos - self.CENTER)
            if self.grid[tuple(map_pos)] == 1 or stop <= length:
                break
            if start <= length:
                self.grid[tuple(map_pos)] = value

    def print_clock(self):
        print(*center(*("".join("  #.;*._|"[value] for value in row)
                        for row in self.grid)), sep="\n")

    def draw_face(self):
        # Boundary
        for theta in np.linspace(0, 2 * np.pi, 100, endpoint=False):
            self.line_segment(theta, start=.95, stop=1, value=2)

        i = True
        # Ticks
        for theta in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            self.line_segment(theta, start=.8 - .1 * i, stop=1, value=2)
            i = not i

    def draw_hands(self):
        hours, minutes, seconds = time.localtime()[3:6]
        tau = 2 * np.pi
        hours = (hours + minutes / 60) % 12
        self.line_segment(angle=tau * hours / 12, start=0, stop=.4, value=5)
        self.line_segment(angle=tau * minutes / 60, start=0, stop=.65, value=4)
        self.line_segment(angle=tau * seconds / 60, start=0, stop=.65, value=3)

    def run(self):
        while True:
            self.reset()

            self.draw_hands()
            self.grid[31:34, 11:35] = digital_time()
            time.sleep(1)
            os.system("clear")
            self.print_clock()

if __name__=="__main__":
    Clock().run()