"""
Just a tiny text-based ConnectFour game.
"""

import numpy as np


class ConnectFour:
    """
    ConnectFour! The first player to connect four checkers in a row wins!
    """
    board = np.zeros((6, 7), dtype=int)
    current_move = None
    current_player = 0

    def print_board(self):
        """
        Print our current board state.
        """
        print("", "╷" + "╷".join("1234567") + "╷",
              *("│" + "│".join(" ●○"[value] for value in row) + "│" for row in self.board),
              "╰" + "─┴" * 6 + "─╯", sep="\n")

    def is_move_valid(self, move=None, automatic=False):
        """
        Returns True if move is a valid move or 'q'.

        'automatic' parameter is so we don't spam players with error messages when checking
        if there are any valid moves left.
        """
        #"Default" value for move is self.current_move
        if move is None:
            if self.current_move is None:
                return False
            move = self.current_move

        if move == 'q':
            return True

        try:
            move = int(move)
        except ValueError:
            print("Please input an integer!")
            return False

        if not 0 < move < 8:
            print("Please choose a column between 1 and 7 (inclusive)!")
            return False

        #Check that a move is possible in given column.
        if not self.board[:, move - 1].all():
            self.current_move = move - 1
            return True
        if not automatic:
            print("No moves possible in that column!")
        return False

    def has_valid_moves(self):
        """
        Returns True if there are still moves left to make in the game.
        """
        return any(self.is_move_valid(move, True) for move in range(1, 8))

    def is_connect_four(self):
        """
        Returns if a player has won.
        """
        #Look right
        #Bottom rows more likely to have four-in-a-row, so start there
        if any((self.board[row, column:column + 4] == self.current_player + 1).all()
               for row in range(5, -1, -1) for column in (0, 1, 2, 3)):
            return True

        #Look up
        if any((self.board[row - 3:row + 1, column] == self.current_player + 1).all()
               for row in (5, 4, 3) for column in range(7)):
            return True

        #Look up-right
        if any(all(self.board[row - i, column + i] == self.current_player + 1 for i in range(4))
               for row in (5, 4, 3) for column in (0, 1, 2, 3)):
            return True

        #Look up-left:
        if any(all(self.board[row - i, column - i] == self.current_player + 1 for i in range(4))
               for row in (5, 4, 3) for column in (3, 4, 5, 6)):
            return True

        #Other directions taken care of by symmetry
        return False

    def update_board(self):
        """
        Add a checker at the lowest position possible in a column.
        """
        column = self.board[:, self.current_move]
        self.board[np.argmax(np.where(column == 0)), self.current_move] = self.current_player + 1

    def start(self):
        """
        The main game loop.
        """
        while self.has_valid_moves():

            self.current_move = None

            self.print_board()

            while not self.is_move_valid():
                self.current_move = input((f"{'●○'[self.current_player]}'s move, "
                                           "please enter column number or 'q' to quit: ")).lower()
            if self.current_move == "q":
                break

            self.update_board()

            if self.is_connect_four():
                self.print_board()
                print(f"{'●○'[self.current_player]} wins!")
                break

            self.current_player = not self.current_player

        else:
            self.print_board()
            print("It's a draw!")

if __name__ == "__main__":
    ConnectFour().start()
