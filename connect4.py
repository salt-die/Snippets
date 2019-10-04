"""
Just a tiny text-based ConnectFour game.
"""

import os
from itertools import product
import numpy as np

TERMSIZE = os.get_terminal_size().columns

def center(*lines):
    """
    Center lines in terminal.
    """
    for line in lines:
        yield line.center(TERMSIZE)

def print_line(line):
    """
    Print line centered in terminal.
    """
    print(*center(line))

class ConnectFour:
    """
    ConnectFour! The first player to connect four checkers in a row wins!
    """
    def __init__(self, height=6, width=7):
        self.height, self.width = height, width
        self.labels = "1234567890abcdefghijklmnoprstuvwxyz"[:width]
        self.board = np.zeros((height, width), dtype=int)
        self.current_move = None
        self.current_player = 0
        self.checkers_in_column = [0] * width

    def print_board(self):
        """
        Print our current board state.
        """
        os.system("clear || cls")  # Clears the terminal

        header = f"╷{'╷'.join(self.labels)}╷"
        gutter = (f"│{'│'.join(' ●○'[value] for value in row)}│" for row in self.board)
        footer = f"╰{'─┴' * (self.width - 1)}─╯"
        print(*center(header, *gutter, footer), sep="\n")

    def is_move_valid(self):
        """
        Returns True if self.current_move is a valid move or 'q'.
        """

        if self.current_move is None:
            return False

        if self.current_move == 'q':
            return True

        if len(self.current_move) > 1 or self.current_move not in self.labels:
            print_line("Please input a valid column!")
            return False

        self.current_move = self.labels.find(self.current_move)

        # Check that a move is possible in given column.
        if self.checkers_in_column[self.current_move] < self.height:
            return True

        print_line("No moves possible in that column!")
        return False

    def is_connect_four(self):
        """
        Returns True if a player has won.
        """
        # Location of our last checker
        row, column = self.height - self.checkers_in_column[self.current_move], self.current_move

        player = self.current_player + 1

        # Look Down
        if row + 4 <= self.height and (self.board[row:row + 4, column] == player).all():
            return True

        # Look Right
        for x in (column - i for i in range(3) if column - i >= 0):
            if x + 4 <= self.width and (self.board[row, x:x + 4] == player).all():
                return True

        # Look Left
        for x in (column + i for i in range(3) if column + i <= self.width):
            if x - 3 >= 0 and (self.board[row, x - 3:x + 1] == player).all():
                return True

        def diagonal(y_step, x_step):
            """
            If our cell is at the '1':

               O O O O X
               O O O X O
               O O 1 O O
               O 2 O O O
               3 O O O O

            and we're checking the diagonal in the direction of the 'X', we'll also check the
            same diagonal in the cell located at '2' and '3'. This should cover cases where
            the last checker placed in a four-in-a-row is not at the ends.
            """
            for y, x in ((row - y_step * i, column - x_step * i) for i in range(3)):

                if not all((0 <= y < self.height, 0 <= y + 3 * y_step < self.height,
                            0 <= x < self.width, 0 <= x + 3 * x_step < self.width)):
                    continue

                if all(self.board[y + y_step * i, x + x_step * i] == player for i in range(4)):
                    return True

            return False

        if any(diagonal(*steps) for steps in product((-1, 1), repeat=2)):
            return True

        return False

    def update_board(self):
        """
        Add a checker at the lowest position possible in a column.
        """
        self.checkers_in_column[self.current_move] += 1
        self.board[self.height - self.checkers_in_column[self.current_move],
                   self.current_move] = self.current_player + 1

    def start(self):
        """
        The main game loop.
        """
        for _ in range(self.width * self.height):

            self.current_move = None

            self.print_board()

            while not self.is_move_valid():
                print_line(f"{'●○'[self.current_player]}'s move,"
                           "enter column or 'q' to quit:\n")
                self.current_move = input("".center(TERMSIZE // 2)).lower()
            if self.current_move == "q":
                break

            self.update_board()

            if self.is_connect_four():
                self.print_board()
                print_line(f"{'●○'[self.current_player]} wins!")
                break

            self.current_player = not self.current_player

        else:
            self.print_board()
            print_line("It's a draw!")


if __name__ == "__main__":
    try:
        width = int(input("Number of columns: "))
        if width > 35:  # Not enough labels -- add more if you want more columns.
            raise ValueError
    except ValueError:
        width = 7

    try:
        height = int(input("Number of rows: "))
    except ValueError:
        height = 6

    ConnectFour(height, width).start()
