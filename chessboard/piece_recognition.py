import chess
from chess import Board, Move
from copy import deepcopy

class ChessGameSimulator:
    def __init__(self):
        self.board = Board()
        self.holm = [self._board_to_matrix(self.board)]
        self.hotm = [self.holm[-1]]
        self.game_started = False
        self.promotion_pending = False
        self.promotion_move = None
        self.promotion_choice = None

    def update_from_sensor(self, lattice_reading):
        """Update with new sensor reading and maintain HOTM history"""
        self.hotm.append(deepcopy(lattice_reading))
        if not self.game_started:
            self.game_started = (lattice_reading == self.holm[0])

    def is_state_correct(self):
        """Check if current HOTM state matches any legal move"""
        try:
            source, dest, _ = detect_move(self.holm[-1], self.hotm)
            return source is not None and dest is not None
        except:
            return False

    def push_move(self):
        """Updated to use detected move"""
        if not self.game_started:
            return False

        detected = detect_move(self.holm[-1], self.hotm)
        legal_move = find_legal_move(self.board, detected)

        if legal_move:
            # Handle promotion
            if legal_move.promotion:
                self.promotion_pending = True
                self.promotion_move = legal_move
                return "promotion_needed"

            self.board.push(legal_move)
            self._update_state()
            return True
        return False

    def finalize_promotion(self, choice):
        """Call this when promotion choice is selected"""
        if not self.promotion_pending:
            return False

        promoted_move = Move(self.promotion_move.from_square,
                             self.promotion_move.to_square,
                             promotion=choice)
        self.board.push(promoted_move)
        self._update_state()
        self.promotion_pending = False
        return True

    def get_missing_start_pieces(self, current_matrix):
        """Compare with standard initial position, return missing squares"""
        initial_matrix = self._board_to_matrix(Board())
        missing = []
        for rank in [0, 1, 6, 7]:  # First 2 and last 2 ranks
            for file in range(8):
                if initial_matrix[rank][file] == 1 and current_matrix[rank][file] == 0:
                    chess_rank = 8 - rank
                    chess_file = chr(ord('A') + file)
                    missing.append(f"{chess_file}{chess_rank}")
        return missing

    def validate_initial_position(self, current_matrix):
        """Check if all start pieces are present"""
        return len(self.get_missing_start_pieces(current_matrix)) == 0

    def _update_state(self):
        self.holm.append(deepcopy(self.hotm[-1]))
        self.hotm = [deepcopy(self.holm[-1])]

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
        return self.board



# Add these methods to ChessGameSimulator class:
def get_missing_start_pieces(self, current_matrix):
    """Compare with standard initial position, return missing squares"""
    initial_matrix = self._board_to_matrix(Board())
    missing = []

    # Check only first 2 and last 2 ranks
    for rank in [0, 1, 6, 7]:
        for file in range(8):
            if initial_matrix[rank][file] == 1 and current_matrix[rank][file] == 0:
                # Convert to chess notation
                chess_rank = 8 - rank
                chess_file = chr(ord('A') + file)
                missing.append(f"{chess_file}{chess_rank}")
    return missing


def validate_initial_position(self, current_matrix):
    """Check if all start pieces are present"""
    return len(self.get_missing_start_pieces(current_matrix)) == 0

def get_captured_square(board, move):
    if board.is_en_passant(move):
        to_rank = chess.square_rank(move.to_square)
        to_file = chess.square_file(move.to_square)
        captured_rank = to_rank - 1 if board.turn == chess.WHITE else to_rank + 1
        return chess.square(to_file, captured_rank)
    elif board.is_capture(move):
        return move.to_square
    return None


def detect_move(legal_board, hotm_list):
    # Convert all matrices in HOTM to chess.Board states
    hotm_states = []
    for matrix in hotm_list:
        board = chess.Board()
        board.clear()
        for r in range(8):
            for c in range(8):
                if matrix[r][c]:
                    # Place a generic piece (type doesn't matter for our binary detection)
                    board.set_piece_at(chess.square(c, 7 - r), chess.Piece(chess.PAWN, chess.WHITE))
        hotm_states.append(board)

    # Find all square changes through HOTM steps
    move_sequence = []
    for i in range(1, len(hotm_states)):
        prev = hotm_states[i - 1]
        curr = hotm_states[i]
        moved = list(prev.squares ^ curr.squares)
        if len(moved) == 2:
            # Simple move
            move_sequence.append((moved[0], moved[1]))
        elif len(moved) == 3:
            # Capture move
            captured = list(set(prev.squares) - set(curr.squares))[0]
            move_sequence.append((moved[0], moved[1], captured))

    # Reconstruct move from sequence
    final_move = None
    if move_sequence:
        # Get first and last squares from sequence
        from_sq = move_sequence[0][0]
        to_sq = move_sequence[-1][1]
        captured_sq = move_sequence[-1][2] if len(move_sequence[-1]) > 2 else None

        # Convert to chess.Move
        final_move = chess.Move(from_sq, to_sq)
        final_move.captured = captured_sq

    return final_move


def find_legal_move(chess_board, detected_move):
    """Find a legal move matching detected move trajectory and captures"""
    if not detected_move:
        return None

    for move in chess_board.generate_legal_moves():
        if (move.from_square == detected_move.from_square and
                move.to_square == detected_move.to_square):
            # Check captures
            actual_captured = get_captured_square(chess_board, move)
            if actual_captured == detected_move.captured:
                return move
    return None