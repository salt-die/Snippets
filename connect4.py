"""
Just a tiny text-based ConnectFour game.
"""

import os
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
        Returns True if move is a valid move or 'q'.

        'automatic' parameter is so we don't spam players with error messages when checking
        if there are any valid moves left.
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
        # Location of our last move
        row, column = HEIGHT - self.checkers_in_column[self.current_move], self.current_move

        # Look right
        if column + 4 <= WIDTH:
            if (self.board[row, column:column + 4] == self.current_player + 1).all():
                return True

        #Look left
        if column - 3 >= 0:
            if (self.board[row, column - 3:column + 1] == self.current_player + 1).all():
                return True

        # Look down
        if row + 4 <= HEIGHT:
            if (self.board[row:row + 4, column] == self.current_player + 1).all():
                return True

        # We don't look up -- how would one place a checker at the bottom of a 4-in-a-row?

        # Look up-right
        if row - 3 >= 0 and column + 4 <= WIDTH:
            if all(self.board[row - i, column + i] == self.current_player + 1 for i in range(4)):
                   return True

        # Look up-left:
        if row - 3 >= 0 and column - 3 >= 0:
            if all(self.board[row - i, column - i] == self.current_player + 1 for i in range(4)):
                   return True

        # Look down-right
        if row + 4 <= HEIGHT and column + 4 <= WIDTH:
            if all(self.board[row + i, column + i] == self.current_player + 1 for i in range(4)):
                return True

        # Look down-left
        if row + 4 <= HEIGHT and column - 3 >= 0:
            if all(self.board[row + i, column - i] == self.current_player + 1 for i in range(4)):
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
