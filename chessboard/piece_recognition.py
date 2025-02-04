import chess


class Chessboard:
    def __init__(self):
        self.board = chess.Board()
        self.lattice_reading = None
        self.correct_state = False
        self.expected_matrix = self._board_to_matrix(self.board)

    def update_from_sensor(self, lattice_reading):
        """Update the internal state with sensor reading and validate position"""
        self.lattice_reading = lattice_reading

        if not self.correct_state:
            # Check if initial setup matches
            self.correct_state = (self.lattice_reading == self.expected_matrix)

    def is_state_correct(self):
        """Return the validation state of the board"""
        return self.correct_state

    def push_move(self):
        """Attempt to update board state based on sensor reading and legal moves"""
        if not self.correct_state or self.lattice_reading is None:
            return False

        # Generate all possible next positions
        legal_moves = list(self.board.legal_moves)
        for move in legal_moves:
            temp_board = self.board.copy()
            temp_board.push(move)

            if self._board_to_matrix(temp_board) == self.lattice_reading:
                self.board.push(move)
                self.expected_matrix = self.lattice_reading
                return True

        return False

    def _board_to_matrix(self, board):
        """Convert chess.Board to binary matrix representation"""
        matrix = []
        for rank in range(7, -1, -1):
            row = []
            for file in range(8):
                square = chess.square(file, rank)
                row.append(1 if board.piece_at(square) else 0)
            matrix.append(row)
        return matrix

    def get_current_board(self):
        """Return the internal python-chess board object"""
        return self.board