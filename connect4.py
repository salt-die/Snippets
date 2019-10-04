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
        row, column = HEIGHT - self.checkers_in_column[self.current_move], self.current_move

        player = self.current_player + 1

        # Look Down
        if row + 4 <= HEIGHT and (self.board[row:row + 4, column] == player).all():
            return True

        # Look Right
        for x in (column - i for i in range(3) if column - i >= 0):
            if x + 4 <= WIDTH and (self.board[row, x:x + 4] == player).all():
                return True

        # Look Left
        for x in (column + i for i in range(3) if column + i <= WIDTH):
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

                if not all((0 <= y < HEIGHT, 0 <= y + 3 * y_step < HEIGHT,
                            0 <= x < WIDTH, 0 <= x + 3 * x_step < WIDTH)):
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
