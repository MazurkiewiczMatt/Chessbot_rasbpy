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
        """Updated to handle promotions"""
        if not self.game_started or len(self.hotm) < 2:
            return False

        source, dest, captured_square = detect_move(self.holm[-1], self.hotm)
        # Remove captured_square from the call
        legal_move = find_legal_move(self.board, self.hotm[-1])

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

def detect_move(legal_board, hotm_list):
    final_board = hotm_list[-1]
    source, dest, captured_square = None, None, None

    # Find source and destination
    for r in range(8):
        for c in range(8):
            if legal_board[r][c] != final_board[r][c]:
                if legal_board[r][c] == 1 and final_board[r][c] == 0:
                    source = (r, c)
                elif legal_board[r][c] == 0 and final_board[r][c] == 1:
                    dest = (r, c)

    # Check for standard captures (destination was occupied)
    if dest and legal_board[dest[0]][dest[1]] == 1:
        for step in hotm_list:
            if step[dest[0]][dest[1]] == 0:
                captured_square = dest
                break

    # Check for en passant or other captures (squares cleared in HOTM)
    if not captured_square:
        candidates = []
        for r in range(8):
            for c in range(8):
                if legal_board[r][c] == 1 and final_board[r][c] == 0:
                    for step in hotm_list:
                        if step[r][c] == 0:
                            candidates.append((r, c))
                            break
        if len(candidates) == 1:
            captured_square = candidates[0]

    return source, dest, captured_square


def get_captured_square(board, move):
    if board.is_en_passant(move):
        to_rank = chess.square_rank(move.to_square)
        to_file = chess.square_file(move.to_square)
        captured_rank = to_rank - 1 if board.turn == chess.WHITE else to_rank + 1
        return chess.square(to_file, captured_rank)
    elif board.is_capture(move):
        return move.to_square
    return None


def find_legal_move(chess_board, final_board):
    """Find a legal move that results in the final_board state."""
    for move in chess_board.legal_moves:
        # Simulate the move on a copy of the board
        board_copy = chess_board.copy()
        board_copy.push(move)
        # Generate the matrix after the move
        simulated = ChessGameSimulator()._board_to_matrix(board_copy)
        if simulated == final_board:
            return move
    return None