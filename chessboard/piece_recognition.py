import numpy as np
import chess

# Define piece constants
EMPTY = 0
WHITE_PAWN = 1
WHITE_KNIGHT = 2
WHITE_BISHOP = 3
WHITE_ROOK = 4
WHITE_QUEEN = 5
WHITE_KING = 6
BLACK_PAWN = -1
BLACK_KNIGHT = -2
BLACK_BISHOP = -3
BLACK_ROOK = -4
BLACK_QUEEN = -5
BLACK_KING = -6


class Chessboard:
    def __init__(self):
        # Initialize the chessboard with pieces represented by integers
        self.board_matrix = np.array([
            [BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK],
            [BLACK_PAWN] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [WHITE_PAWN] * 8,
            [WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK],
        ])

        # Store history of positions (as NumPy arrays)
        self.history = [self.board_matrix.copy()]

        # Temporary history for moves within a turn
        self.temp_history = []

        # Initialize the chess.Board() from python-chess
        self.chess_board = chess.Board()

        # Keep track of whose turn it is: True for White, False for Black
        self.white_to_move = True

    def get_current_board(self):
        return self.board_matrix

    def save_position(self):
        # Append the current position to the permanent history
        self.history.append(self.board_matrix.copy())
        # Clear temporary history
        self.temp_history.clear()
        # Switch turn
        self.white_to_move = not self.white_to_move

    def add_to_temp(self, new_board_matrix):
        # Add a new board state to the temporary history
        self.temp_history.append(np.array(new_board_matrix))

    def estimate_move(self):
        # Compare the last position in history with the last in temp_history
        if not self.temp_history:
            print("No temporary history to estimate move from.")
            return None  # No moves to estimate

        prev_board = self.history[-1]
        current_board = self.temp_history[-1]

        # Find squares where the board has changed
        diff = current_board - prev_board

        # Get indices where the board has changed
        changed_positions = np.argwhere(diff != 0)

        print("Changed positions (row, col):", changed_positions)

        # For debugging: show what pieces have been picked up and from where
        for pos in changed_positions:
            row, col = pos
            prev_piece = prev_board[row, col]
            curr_piece = current_board[row, col]
            square = self.matrix_to_square(pos)
            print(f"Square {square} changed from {prev_piece} to {curr_piece}")

        # Depending on the number of changes, determine the move
        if len(changed_positions) == 2:
            # Normal move or capture
            from_pos = None
            to_pos = None
            for pos in changed_positions:
                row, col = pos
                prev_piece = prev_board[row, col]
                curr_piece = current_board[row, col]
                if prev_piece != EMPTY and curr_piece == EMPTY:
                    # Piece moved from here
                    from_pos = pos
                elif prev_piece == EMPTY and curr_piece != EMPTY:
                    # Piece moved to here
                    to_pos = pos
            if from_pos is not None and to_pos is not None:
                from_square = self.matrix_to_square(from_pos)
                to_square = self.matrix_to_square(to_pos)
                move_uci = from_square + to_square
                # Check for promotions (pawn reaches last rank)
                moved_piece = prev_board[from_pos[0], from_pos[1]]
                if abs(moved_piece) == WHITE_PAWN or abs(moved_piece) == BLACK_PAWN:
                    if (to_pos[0] == 0 and moved_piece > 0) or (to_pos[0] == 7 and moved_piece < 0):
                        # Assume promotion to Queen for simplicity
                        move_uci += 'q'
                return move_uci
            else:
                print("Could not determine from and to positions.")
                return None
        elif len(changed_positions) == 4:
            # Possibly castling
            # Need to detect castling move
            # In castling, both the king and rook move
            moved_pieces = []
            for pos in changed_positions:
                row, col = pos
                prev_piece = prev_board[row, col]
                curr_piece = current_board[row, col]
                moved_pieces.append((prev_piece, curr_piece, pos))

            # Check if the king and rook have moved in expected castling pattern
            if self.detect_castling(moved_pieces):
                # Determine if it's kingside or queenside castling
                # For UCI notation, castling is represented by king's move
                king_from_pos = None
                king_to_pos = None
                for prev_piece, curr_piece, pos in moved_pieces:
                    if abs(prev_piece) == WHITE_KING and curr_piece == EMPTY:
                        king_from_pos = pos
                    elif abs(curr_piece) == WHITE_KING and prev_piece == EMPTY:
                        king_to_pos = pos
                if king_from_pos is not None and king_to_pos is not None:
                    from_square = self.matrix_to_square(king_from_pos)
                    to_square = self.matrix_to_square(king_to_pos)
                    move_uci = from_square + to_square
                    return move_uci
                else:
                    print("Could not determine king's positions in castling.")
                    return None
            else:
                print("Four changes detected but not castling.")
                return None
        else:
            print("Number of changed positions not recognized for a legal move.")
            return None

    def detect_castling(self, moved_pieces):
        # Check if the moved pieces correspond to castling
        positions = {}
        for prev_piece, curr_piece, pos in moved_pieces:
            positions[(prev_piece, curr_piece)] = pos

        # Check for white castling
        if self.white_to_move:
            # King from e1 to g1 (kingside) or c1 (queenside)
            # Rook from h1 to f1 (kingside) or a1 to d1 (queenside)
            king_initial_pos = np.array([7, 4])
            kingside_rook_initial_pos = np.array([7, 7])
            queenside_rook_initial_pos = np.array([7, 0])
            king_final_positions = [np.array([7, 6]), np.array([7, 2])]
            rook_final_positions = [np.array([7, 5]), np.array([7, 3])]

            king_moved = False
            rook_moved = False
            for (prev_piece, curr_piece), pos in positions.items():
                if prev_piece == WHITE_KING and curr_piece == EMPTY and (pos == king_initial_pos).all():
                    king_moved = True
                elif prev_piece == EMPTY and curr_piece == WHITE_KING and any(
                        (pos == kp).all() for kp in king_final_positions):
                    king_moved = True
                elif prev_piece == WHITE_ROOK and curr_piece == EMPTY and (pos == kingside_rook_initial_pos).all():
                    rook_moved = True
                elif prev_piece == EMPTY and curr_piece == WHITE_ROOK and any(
                        (pos == rp).all() for rp in rook_final_positions):
                    rook_moved = True
            if king_moved and rook_moved:
                return True
        else:
            # Similar checks for black castling
            king_initial_pos = np.array([0, 4])
            kingside_rook_initial_pos = np.array([0, 7])
            queenside_rook_initial_pos = np.array([0, 0])
            king_final_positions = [np.array([0, 6]), np.array([0, 2])]
            rook_final_positions = [np.array([0, 5]), np.array([0, 3])]

            king_moved = False
            rook_moved = False
            for (prev_piece, curr_piece), pos in positions.items():
                if prev_piece == BLACK_KING and curr_piece == EMPTY and (pos == king_initial_pos).all():
                    king_moved = True
                elif prev_piece == EMPTY and curr_piece == BLACK_KING and any(
                        (pos == kp).all() for kp in king_final_positions):
                    king_moved = True
                elif prev_piece == BLACK_ROOK and curr_piece == EMPTY and (pos == kingside_rook_initial_pos).all():
                    rook_moved = True
                elif prev_piece == EMPTY and curr_piece == BLACK_ROOK and any(
                        (pos == rp).all() for rp in rook_final_positions):
                    rook_moved = True
            if king_moved and rook_moved:
                return True

        return False

    def matrix_to_square(self, position):
        # Convert matrix indices to chess square notation
        row, col = position
        file = chr(ord('a') + col)
        rank = str(8 - row)
        return file + rank

    def is_move_legal(self, move_uci):
        move = chess.Move.from_uci(move_uci)
        legal = move in self.chess_board.legal_moves
        if not legal:
            print(f"Move {move_uci} is not legal.")
        return legal

    def make_move(self):
        move_uci = self.estimate_move()
        if move_uci is None:
            print("Move estimation failed.")
            return False  # Invalid move

        print(f"Estimated move: {move_uci}")

        # Show list of legal moves
        legal_moves = list(self.chess_board.legal_moves)
        print("Legal moves from python-chess:")
        print([move.uci() for move in legal_moves])

        if self.is_move_legal(move_uci):
            # Make the move on the python-chess board
            self.chess_board.push_uci(move_uci)
            # Update the board matrix to reflect the move
            self.board_matrix = self.temp_history[-1]
            # Save the position to history
            self.save_position()
            print(f"Move made: {move_uci}")
            # Print whose turn it is
            print(f"Next turn: {'White' if self.white_to_move else 'Black'}")
            return True  # Move was legal and made
        else:
            print("Illegal move.")
            return False  # Move was illegal

    def get_history(self):
        # Return the list of moves in UCI notation
        return [move.uci() for move in self.chess_board.move_stack]

    def get_board_fen(self):
        # Return the FEN notation of the current board
        return self.chess_board.fen()
# Initialize the chessboard
chessboard = Chessboard()

# For debugging, print whose turn it is
print(f"Current turn: {'White' if chessboard.white_to_move else 'Black'}")

# Remove pieces between the king and rook to simulate the path being clear
# Remove the knight from g1 (row 7, col 6)
chessboard.board_matrix[7][6] = EMPTY
# Remove the bishop from f1 (row 7, col 5)
chessboard.board_matrix[7][5] = EMPTY

# Update the board in the temp history (starting point for temporary history)
chessboard.add_to_temp(chessboard.board_matrix.copy())

# Now simulate the castling move
# King moves from e1 (row 7, col 4) to g1 (row 7, col 6)
# Rook moves from h1 (row 7, col 7) to f1 (row 7, col 5)
new_board = chessboard.board_matrix.copy()

# King moves
new_board[7][4] = EMPTY  # e1
new_board[7][6] = WHITE_KING  # g1

# Rook moves
new_board[7][7] = EMPTY  # h1
new_board[7][5] = WHITE_ROOK  # f1

# Add the new board state to temporary history
chessboard.add_to_temp(new_board)

# Assume the player clicks the button to finalize the move
chessboard.make_move()

# Output the current board in FEN notation
print("Current Board FEN:", chessboard.get_board_fen())

# Print the move history in UCI notation
print("Move History:", chessboard.get_history())
