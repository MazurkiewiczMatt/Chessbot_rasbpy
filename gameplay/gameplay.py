import chess

class Gameplay:
    PROMOTION_MAP = {
        4: chess.QUEEN,
        5: chess.ROOK,
        6: chess.BISHOP,
        7: chess.KNIGHT
    }

    PROMOTION_NAMES = {
        chess.QUEEN: "QUEEN",
        chess.ROOK: "ROOK",
        chess.BISHOP: "BISHOP",
        chess.KNIGHT: "KNIGHT"
    }

    def __init__(self, chess_game, serial_handler):
        self.chess_game = chess_game
        self.serial_handler = serial_handler


    def handle_promotion_selection(self, buttons_reading):
        """Show promotion options only when pending"""
        if not self.chess_game.promotion_pending:
            return False

        for btn_idx in [4,5,6,7]:
            if buttons_reading[btn_idx]:
                choice = self.PROMOTION_MAP[btn_idx]
                self.chess_game.finalize_promotion(choice)
                self.serial_handler.display_text("PROMOTED TO",
                    self.PROMOTION_NAMES[choice])
                return True

        return False

    def process_button_reading(self, buttons_reading):
        # Handle promotion first
        if self.chess_game.promotion_pending:
            self.handle_promotion_selection(buttons_reading)
            return

        # Handle move confirmation

        if (buttons_reading[0] and self.chess_game.board.turn == chess.WHITE) or (buttons_reading[2] and self.chess_game.board.turn == chess.BLACK):  # M
            self.handle_main_action()
        #elif buttons_reading[0] or buttons_reading[2]:
        #    self.serial_handler.display_text("OTHER GUYS TURN","")


    def handle_main_action(self):
        result = self.chess_game.push_move()
        if result == "promotion_needed":
            self.serial_handler.display_text("PROMOTE: 4=Q 5=R", "6=B 7=N")
        elif result:
            move = self.chess_game.board.peek().uci()
            self.serial_handler.display_text("MOVED", move[:14])
        else:
            self.serial_handler.display_text("INVALID MOVE", "ADJUST BOARD")

    def missing(self,lattice_reading, chess_game):
        missing = chess_game.get_missing_start_pieces(lattice_reading)

        # Replace the missing pieces display logic with:
        if 0 < len(missing) <= 4:
            # Split missing squares into chunks of 2
            chunks = [missing[i:i + 2] for i in range(0, len(missing), 2)]
            # Format with proper spacing
            line1 = " ".join(chunks[0]).ljust(14) if len(chunks) > 0 else ""
            line2 = " ".join(chunks[1]).ljust(14) if len(chunks) > 1 else ""
            self.serial_handler.display_text(line1[:14], line2[:14])

        elif len(missing) > 4:
            self.serial_handler.display_text("XD MISSING", f"{len(missing)} PIECES")



