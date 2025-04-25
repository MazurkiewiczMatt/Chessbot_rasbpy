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
        try:
            detected = detect_move(self.holm[-1], self.hotm)  # ← pass HOTM
            return bool(find_legal_move(self.board, detected))
        except Exception:
            return False

    def push_move(self):
        if not self.game_started:
            return False

        detected    = detect_move(self.holm[-1], self.hotm)   # ← pass HOTM
        legal_move  = find_legal_move(self.board, detected)
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

def _leave_index(hotm, rank, file):
    """Index of the first frame where (rank,file) becomes empty."""
    for idx, mat in enumerate(hotm[1:], 1):           # skip frame 0 (legal pos.)
        if mat[rank][file] == 0:
            return idx
    return None


def _infer_captured_square(initial_matrix, hotm, mover_sq):
    """
    Return the square index of a captured piece, or None.
    Uses the same logic as in the previous patch: anything that emptied *before*
    the mover left counts as the capture square.
    """
    mr, mf = 7 - chess.square_rank(mover_sq), chess.square_file(mover_sq)
    mover_leave = _leave_index(hotm, mr, mf)
    if mover_leave is None:
        return None

    earliest_cap, earliest_idx = None, mover_leave
    for rank in range(8):
        for file in range(8):
            if (rank, file) == (mr, mf):
                continue
            if initial_matrix[rank][file] == 0:
                continue
            idx = _leave_index(hotm, rank, file)
            if idx is not None and 0 < idx < earliest_idx:
                earliest_idx, earliest_cap = idx, chess.square(file, 7 - rank)
    return earliest_cap


def _detect_castling(from_squares, to_squares):
    """
    If {from_squares,to_squares} correspond to castling, return king Move.
    Otherwise return None.
    """
    for f in from_squares:
        for t in to_squares:
            same_rank = chess.square_rank(f) == chess.square_rank(t)
            if same_rank and abs(chess.square_file(f) - chess.square_file(t)) == 2:
                # king moves two files horizontally – that’s castling
                return Move(f, t)
    return None


# ---------------------------------------------------------------------------
# main detector
# ---------------------------------------------------------------------------

def detect_move(initial_matrix, hotm):
    """
    Determine the move that occurred given a legal position (initial_matrix)
    and a list of raw-sensor frames since that position (hotm).

    Returns
    -------
    chess.Move | None
        A move with .captured optionally set; .promotion left to 0 (unset).
    """
    final_matrix = hotm[-1]

    moved_from, moved_to = [], []
    for rank in range(8):
        for file in range(8):
            was_piece = initial_matrix[rank][file] == 1
            is_piece  = final_matrix[rank][file] == 1
            if was_piece and not is_piece:
                moved_from.append(chess.square(file, 7 - rank))
            elif not was_piece and is_piece:
                moved_to.append(chess.square(file, 7 - rank))

    # ------------------------------------------------------------------ castling
    if len(moved_from) == 2 and len(moved_to) == 2:
        castle_move = _detect_castling(moved_from, moved_to)
        if castle_move:
            return castle_move            # board.push() will move the rook too

    # -------------------------------------------------------- normal / captures
    if len(moved_from) == 1 and len(moved_to) == 1:
        from_sq, to_sq = moved_from[0], moved_to[0]
        move           = Move(from_sq, to_sq)
        move.captured  = _infer_captured_square(initial_matrix, hotm, from_sq)
        return move

    # ---------------------------------------------------------- en-passant etc.
    if len(moved_from) == 2 and len(moved_to) == 1:
        # Two squares emptied, one filled → capture where the *earlier* empty
        # square is the captured pawn (en-passant or normal capture confusion).
        # Identify the mover: the square that was lifted *later*.
        idx_a = _leave_index(hotm, 7 - chess.square_rank(moved_from[0]),
                                   chess.square_file(moved_from[0]))
        idx_b = _leave_index(hotm, 7 - chess.square_rank(moved_from[1]),
                                   chess.square_file(moved_from[1]))
        from_sq = moved_from[0] if idx_a > idx_b else moved_from[1]
        to_sq   = moved_to[0]
        move          = Move(from_sq, to_sq)
        move.captured = _infer_captured_square(initial_matrix, hotm, from_sq)
        return move

    # Anything else is either noise or an illegal sensor combination
    return None

def get_captured_square(board, move):
    if board.is_en_passant(move):
        return chess.square(move.to_square.file, move.from_square.rank)
    elif board.is_capture(move):
        return move.to_square
    return None