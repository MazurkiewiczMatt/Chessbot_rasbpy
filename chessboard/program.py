import chess
import copy


def matrix_to_chess_square(pos, board_size=8):
    """
    Convert a matrix coordinate (row, col) to a chess square.
    For an 8x8 board, row 0 corresponds to rank 8, row 7 to rank 1.
    For our 2x2 demo, we assume row 0 -> rank2 and row 1 -> rank1,
    and column 0 -> file 'a', column 1 -> file 'b'.
    """
    file = chr(ord('a') + pos[1])
    rank = str(board_size - pos[0])
    return file + rank


def binary_board_from_chess_board(chess_board, board_size=8):
    """
    Convert a python-chess Board into a binary occupancy matrix.
    Each square is 1 if there is any piece, 0 if empty.
    The matrix is row-major with row 0 being the top.
    """
    binary_board = []
    for r in range(board_size):
        row = []
        for c in range(board_size):
            # chess.square: files 0..7 (a-h), ranks 0..7 (1-8) but note:
            # top row (r==0) corresponds to rank board_size (e.g. 8 in standard chess).
            square = chess.square(c, board_size - 1 - r)
            row.append(1 if chess_board.piece_at(square) else 0)
        binary_board.append(row)
    return binary_board


def detect_move(legal_board, hotm_list):
    """
    Given the last legal (confirmed) board (legal_board)
    and the list of temporary boards (hotm_list) during this turn,
    detect the move by comparing the starting board and final board.

    Returns a tuple (source, dest) where each is a (row, col) index.

    For non-capture moves, one square will change from 1 to 0 (source)
    and one from 0 to 1 (destination). For captures (where the destination
    was already occupied in the legal board) we check intermediate hotm states
    to see which square went empty temporarily.
    """
    final_board = hotm_list[-1]
    source = None
    dest = None

    # First pass: compare legal_board and final_board.
    for r in range(len(legal_board)):
        for c in range(len(legal_board[r])):
            if legal_board[r][c] != final_board[r][c]:
                # A piece has been removed: candidate for the source.
                if legal_board[r][c] == 1 and final_board[r][c] == 0:
                    source = (r, c)
                # A piece has been added: candidate for the destination.
                elif legal_board[r][c] == 0 and final_board[r][c] == 1:
                    dest = (r, c)

    # If no new piece is seen (capture move) then search the hotm history
    # for a square that was temporarily empty before ending as occupied.
    if dest is None:
        for board in hotm_list[1:]:
            for r in range(len(board)):
                for c in range(len(board[r])):
                    if legal_board[r][c] == 1 and board[r][c] == 0 and final_board[r][c] == 1:
                        dest = (r, c)
                        break
                if dest is not None:
                    break
            if dest is not None:
                break

    return source, dest


def find_legal_move(chess_board, final_board, board_size=8):
    """
    Given the current legal position (as a python-chess Board) and the final binary board,
    simulate every legal move and check which one produces a binary board that matches final_board.
    Returns the move (as a chess.Move) if found, else None.
    """
    for move in chess_board.legal_moves:
        board_copy = chess_board.copy()
        board_copy.push(move)
        simulated_board = binary_board_from_chess_board(board_copy, board_size)
        if simulated_board == final_board:
            return move
    return None


class ChessGameSimulator:
    def __init__(self, board_size=8):
        self.board_size = board_size
        # For a full game, we start with the standard chess board.
        self.board = chess.Board()
        # holm stores legal positions (as binary boards)
        self.holm = [binary_board_from_chess_board(self.board, board_size)]
        # hotm stores temporary positions read from the lattice.
        self.hotm = [self.holm[-1]]

    def update_hotm(self, new_board):
        """
        Update the temporary move history with a new lattice reading.
        new_board should be a binary matrix (list of lists).
        """
        self.hotm.append(new_board)

    def button_click(self):
        """
        Simulate clicking the "next turn" button.
        This function:
         1. Takes the last legal board (holm[-1]) and the current temporary history (hotm)
         2. Detects the source and destination squares from the change.
         3. Converts them into chess square names.
         4. Uses python-chess to find which legal move produces the observed final board.
         5. If a legal move is found, updates the game (pushes the move and appends the new board to holm).
        """
        # For this turn, our starting board is the last legal board.
        legal_board = self.holm[-1]
        final_board = self.hotm[-1]

        # Detect source and destination squares based on binary differences.
        source, dest = detect_move(legal_board, self.hotm)
        if source is None or dest is None:
            print("Move detection failed. Incomplete move information.")
            return

        source_square = matrix_to_chess_square(source, self.board_size)
        dest_square = matrix_to_chess_square(dest, self.board_size)
        move_estimation = source_square + dest_square
        print("Estimated move based on binary readings:", move_estimation)

        # Now use python-chess legal moves to check if one of them produces final_board.
        legal_move = find_legal_move(self.board, final_board, self.board_size)
        if legal_move:
            print("Legal move confirmed by engine:", legal_move.uci())
            # Update the chess board and holm history.
            self.board.push(legal_move)
            self.holm.append(final_board)
            # Reset hotm for the next turn (starting with the new legal board).
            self.hotm = [final_board]
        else:
            print("No legal move matches the detected board state.")



def simulate():
    # Create an 8x8 game simulator
    simulator = ChessGameSimulator(board_size=8)

    # Get the initial board state (standard starting position)
    initial_board = simulator.holm[0]

    # Simulate the pawn moving from e2 to e4 by updating HOTM readings
    # Step 1: Pawn is lifted from e2 (source becomes 0)
    reading1 = copy.deepcopy(initial_board)
    reading1[6][4] = 0  # e2 is matrix position (6,4)
    simulator.update_hotm(reading1)

    # Step 2: Pawn is placed on e4 (destination becomes 1)
    reading2 = copy.deepcopy(reading1)
    reading2[4][5] = 1  # e4 is matrix position (4,4)
    simulator.update_hotm(reading2)
    reading2[4][5] = 0  # e4 is matrix position (4,4)
    simulator.update_hotm(reading2)
    reading2[6][4] = 1  # e4 is matrix position (4,4)
    simulator.update_hotm(reading2)

    reading2[6][4] = 0  # e4 is matrix position (4,4)
    simulator.update_hotm(reading2)




    reading2[4][4] = 1  # e4 is matrix position (4,4)
    simulator.update_hotm(reading2)




    # Simulate button click to finalize the turn
    simulator.button_click()

simulate()

