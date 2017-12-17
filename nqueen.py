from copy import deepcopy


class Board:
    """Represents a chess board which keeps track of positions where a queen can be placed."""

    def __init__(self, n, allowed=None):
        """Initialize board dimension and allowed positions."""
        assert isinstance(n, int), "Size must be an integer"
        assert n > 0, "Size must be positive"
        self.dim = n

        if allowed is None:
            self.allowed = [[True for _ in range(n)] for _ in range(n)]
        else:
            self.allowed = allowed

    def place(self, position):
        """Try to place a queen on the given position and return a new board.

        If the queen cannot be placed, return False. Otherwise, return a new board which has
        the board state of the queen being in that position plus the previous state.
        """
        x, y = position
        if not self.allowed[x][y]:
            return False

        updated = deepcopy(self.allowed)
        # Update horizontally and vertically
        for i in range(self.dim):
            updated[x][i] = False
            updated[i][y] = False

        # Update diagonally
        directions = [(1, 1), (1, -1), (-1, 1), (-1, 1)]
        for xdir, ydir in directions:
            row, col = x, y
            while row < self.dim and col < self.dim and row >= 0 and col >= 0:
                updated[row][col] = False
                row += xdir
                col += ydir

        return Board(self.dim, allowed=updated)

    def valid_positions(self, row):
        """Return a list of valid positions for a given row."""
        return [(row, col) for col in range(self.dim) if self.allowed[row][col]]


def nqueen(board, positions=[], row=0, solutions=[], all_solutions=False):
    """Solve the n-queen puzzle recursively for a given board."""
    valids = board.valid_positions(row)
    if not valids:
        return False, None

    for valid in valids:
        # Try to find a solution with queen in this position
        new_board = board.place(valid)
        positions.append(valid)
        if row == board.dim - 1:
            return True, positions
        found, final_positions = nqueen(new_board, positions=positions, row=row + 1)
        if found:
            return True, final_positions
        # There was no solution, keep trying
        positions.pop()
    # No solution found with the given board
    return False, None


def main():
    """Prompt the user for a board size and solve the n-queen puzzle for that board."""
    size = input("Grid size: ")
    size = int(size)
    board = Board(size)
    found, positions = nqueen(board)
    if not found:
        print("No solution found")
    else:
        print("Queen positions:", positions)


if __name__ == "__main__":
    main()
