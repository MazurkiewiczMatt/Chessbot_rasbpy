import chess
from chess import Board, Move
from copy import deepcopy


class ChessGameSimulator:
    def __init__(self):
        self.board = Board()
        self.holm = [self._board_to_matrix(self.board)]  # History of legal matrices
        self.hotm = [self.holm[-1]]  # History of temporary matrices (sensor readings)
        self.game_started = False
        self.promotion_pending = False
        self.promotion_move = None

    def update_from_sensor(self, lattice_reading):
        """Update with new sensor reading and maintain HOTM history"""
        self.hotm.append(deepcopy(lattice_reading))

    def is_state_correct(self):
        """Check if current HOTM state matches any legal move"""
        try:
            detected = detect_move(self.holm[-1], self.hotm[-1])
            return bool(find_legal_move(self.board, detected))
        except:
            return False

    def push_move(self):
        """Push detected move if legal"""
        if not self.game_started:
            return False

        detected = detect_move(self.holm[-1], self.hotm[-1])
        legal_move = find_legal_move(self.board, detected)

        if legal_move:
            if legal_move.promotion:
                self.promotion_pending = True
                self.promotion_move = legal_move
                return "promotion_needed"
            self.board.push(legal_move)
            self._update_state()
            return True
        return False

    def finalize_promotion(self, choice):
        if not self.promotion_pending:
            return False
        promoted_move = Move(self.promotion_move.from_square,
                             self.promotion_move.to_square,
                             promotion=choice)
        self.board.push(promoted_move)
        self._update_state()
        self.promotion_pending = False
        return True

    def _update_state(self):
        self.holm.append(deepcopy(self.hotm[-1]))
        self.hotm = [deepcopy(self.holm[-1])]

    def _board_to_matrix(self, board):
        matrix = []
        for rank in range(7, -1, -1):
            row = []
            for file in range(8):
                square = chess.square(file, rank)
                row.append(1 if board.piece_at(square) else 0)
            matrix.append(row)
        return matrix

    def get_missing_start_pieces(self, current_matrix):
        initial_matrix = self._board_to_matrix(Board())
        missing = []
        for rank in [0, 1, 6, 7]:
            for file in range(8):
                if initial_matrix[rank][file] == 1 and current_matrix[rank][file] == 0:
                    chess_rank = 8 - rank
                    chess_file = chr(ord('A') + file)
                    missing.append(f"{chess_file}{chess_rank}")
        return missing


def detect_move(initial_matrix, final_matrix):
    moved_from = []
    moved_to = []

    for rank in range(8):
        for file in range(8):
            if initial_matrix[rank][file] == 1 and final_matrix[rank][file] == 0:
                moved_from.append((rank, file))
            elif initial_matrix[rank][file] == 0 and final_matrix[rank][file] == 1:
                moved_to.append((rank, file))

    # Convert to chess squares
    from_squares = [chess.square(f, 7 - r) for r, f in moved_from]
    to_squares = [chess.square(f, 7 - r) for r, f in moved_to]

    if len(from_squares) == 1 and len(to_squares) == 1:
        return Move(from_squares[0], to_squares[0])
    elif len(from_squares) == 2 and len(to_squares) == 1:
        # Capture move (detect captured square)
        capture_square = [sq for sq in from_squares if sq != to_squares[0]][0]
        move = Move(from_squares[0], to_squares[0])
        move.captured = capture_square
        return move
    return None


def find_legal_move(board, move):
    if not move:
        return None
    for legal_move in board.generate_legal_moves():
        if (legal_move.from_square == move.from_square and
                legal_move.to_square == move.to_square):
            actual_cap = get_captured_square(board, legal_move)
            if actual_cap == move.captured:
                return legal_move
    return None


def get_captured_square(board, move):
    if board.is_en_passant(move):
        return chess.square(move.to_square.file, move.from_square.rank)
    elif board.is_capture(move):
        return move.to_square
    return None