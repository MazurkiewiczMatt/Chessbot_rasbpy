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

        # Check if game has started (initial position match)
        if not self.game_started:
            self.game_started = (lattice_reading == self.holm[0])

    def is_state_correct(self):
        """Check if current HOTM state matches any legal move"""
        try:
            source, dest = detect_move(self.holm[-1], self.hotm)
            return source is not None and dest is not None
        except:
            return False

    def push_move(self):
        """Updated to handle promotions"""
        if not self.game_started or len(self.hotm) < 2:
            return False

        legal_move = find_legal_move(self.board, self.hotm[-1])
        if legal_move:
            # Check if promotion is needed
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


def detect_move(legal_board, hotm_list):
    final_board = hotm_list[-1]
    source = None
    dest = None

    for r in range(8):
        for c in range(8):
            if legal_board[r][c] != final_board[r][c]:
                if legal_board[r][c] == 1 and final_board[r][c] == 0:
                    source = (r, c)
                elif legal_board[r][c] == 0 and final_board[r][c] == 1:
                    dest = (r, c)

    if dest is None:  # Handle captures
        for board in hotm_list[1:]:
            for r in range(8):
                for c in range(8):
                    if legal_board[r][c] == 1 and board[r][c] == 0 and final_board[r][c] == 1:
                        dest = (r, c)
                        break
                if dest: break
            if dest: break

    return source, dest


def find_legal_move(chess_board, final_board):
    for move in chess_board.legal_moves:
        board_copy = chess_board.copy()
        board_copy.push(move)
        simulated_board = ChessGameSimulator()._board_to_matrix(board_copy)
        if simulated_board == final_board:
            return move
    return None