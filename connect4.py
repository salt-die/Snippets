"""
Just a tiny text-based ConnectFour game.
"""

import os
from itertools import product
import numpy as np

TERMSIZE = os.get_terminal_size().columns
HEIGHT = 6
WIDTH = 7

class ConnectFour:
    """
    ConnectFour! The first player to connect four checkers in a row wins!
    """
    board = np.zeros((HEIGHT, WIDTH), dtype=int)
    current_move = None
    current_player = 0
    checkers_in_column = [0] * WIDTH

    def print_board(self):
        """
        Print our current board state.
        """
        os.system("clear || cls")  # Clears the terminal

        header = f"╷{'╷'.join('1234567')}╷"  # TODO rewrite for variable length
        gutter = (f"│{'│'.join(' ●○'[value] for value in row)}│" for row in self.board)
        footer = f"╰{'─┴' * 6}─╯"
        print(*self.center(header, *gutter, footer), sep="\n")

    @staticmethod
    def center(*lines):
        for line in lines:
            yield line.center(TERMSIZE)

    def print_line(self, line):
        print(*self.center(line))

    def is_move_valid(self):
        """
        Returns True if self.current_move is a valid move or 'q'.
        """

        if self.current_move is None:
            return False

        if self.current_move == 'q':
            return True

        try:
            self.current_move = int(self.current_move)
            self.current_move -= 1
        except ValueError:
            self.print_line("Please input an integer!")
            return False

        if not 0 <= self.current_move < WIDTH:
            self.print_line("Please choose a column between 1 and 7 (inclusive)!")
            return False

        # Check that a move is possible in given column.
        if self.checkers_in_column[self.current_move] < HEIGHT:
            return True

        self.print_line("No moves possible in that column!")
        return False

    def is_connect_four(self):
        """
        Returns True if a player has won.
        """
        # Location of our last checker
        y_loc, x_loc = HEIGHT - self.checkers_in_column[self.current_move], self.current_move

        player = self.current_player + 1

        #Look Down
        if y_loc + 4 <= HEIGHT and (self.board[y_loc:y_loc + 4, x_loc] == player).all():
                return True

        # Loop runs checks for cells close to y_loc, x_loc in case we connect four in the middle
        for row, column in product(range(min(y_loc + 2, HEIGHT - 1), max(y_loc - 3, -1), -1),
                                   range(max(x_loc - 2, 0), min(x_loc + 3, WIDTH))):
            if self.board[row, column] != player:
                continue
            LOOK_RIGHT = column + 4 <= WIDTH
            LOOK_LEFT = column - 3 >= 0
            LOOK_UP = row - 3 >= 0
            LOOK_DOWN = row + 4 <= HEIGHT

            if LOOK_RIGHT and (self.board[row, column:column + 4] == player).all():
                return True

            if LOOK_LEFT and (self.board[row, column - 3:column + 1] == player).all():
                return True

            def diagonal(y_step, x_step):
                return all(self.board[row + y_step * i, column + x_step * i] == player
                           for i in range(4))

            if LOOK_UP and LOOK_RIGHT and diagonal(-1, 1):
                return True

            if LOOK_UP and LOOK_LEFT and diagonal(-1, -1):
                return True

            if LOOK_DOWN and LOOK_RIGHT and diagonal(1, 1):
                return True

            if LOOK_DOWN and LOOK_RIGHT and diagonal(1, -1):
                return True

        return False

    def update_board(self):
        """
        Add a checker at the lowest position possible in a column.
        """
        self.checkers_in_column[self.current_move] += 1
        self.board[HEIGHT - self.checkers_in_column[self.current_move],
                   self.current_move] = self.current_player + 1

    def start(self):
        """
        The main game loop.
        """
        for _ in range(WIDTH * HEIGHT):

            self.current_move = None

            self.print_board()

            while not self.is_move_valid():
                self.print_line(f"{'●○'[self.current_player]}'s move,"
                                "please enter column number or 'q' to quit:\n")
                self.current_move = input("".center(TERMSIZE // 2)).lower()
            if self.current_move == "q":
                break

            self.update_board()

            if self.is_connect_four():
                self.print_board()
                self.print_line(f"{'●○'[self.current_player]} wins!")
                break

            self.current_player = not self.current_player

        else:
            self.print_board()
            self.print_line("It's a draw!")


if __name__ == "__main__":
    ConnectFour().start()
