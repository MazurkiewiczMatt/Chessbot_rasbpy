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

    def process_button_reading(self, buttons_reading):
        # Handle turn completion buttons
        if buttons_reading[0]:  # B0 - White's turn complete
            if self.chess_game.board.turn == chess.WHITE and self.chess_game.board.turn == chess.WHITE:
                self.chess_game.board.turn = chess.BLACK
                self.serial_handler.display_text("TURN ENDED", "BLACK'S TURN")
            else:
                self.serial_handler.display_text("CAN'T END TURN", "MAKE WHITE MOVE")

        if buttons_reading[2]:  # B2 - Black's turn complete
            if self.chess_game.board.turn == chess.BLACK and self.chess_game.board.turn == chess.BLACK:
                self.chess_game.board.turn = chess.WHITE
                self.serial_handler.display_text("TURN ENDED", "WHITE'S TURN")
            else:
                self.serial_handler.display_text("CAN'T END TURN", "MAKE BLACK MOVE")

        # Process promotion selection buttons (4-7)
        promotion_selected = self.handle_promotion_selection(buttons_reading)

        # Handle main action buttons (B1 and B3)
        if any(buttons_reading[i] for i in [1, 3]) and not promotion_selected:
            self.handle_main_action_button()

        # Update turn display after any button interaction
        #self.display_turn_status()

    def display_turn_status(self):
        """Update display with current turn information"""
        if self.chess_game.board.turn == chess.WHITE:
            self.serial_handler.display_text("WHITE'S TURN", "PRESS B0 TO END")
        else:
            self.serial_handler.display_text("BLACK'S TURN", "PRESS B2 TO END")

    def handle_promotion_selection(self, buttons_reading):
        """Process promotion button selections and update display"""
        for btn_idx, pressed in enumerate(buttons_reading):
            if pressed and btn_idx in self.PROMOTION_MAP:
                choice = self.PROMOTION_MAP[btn_idx]
                self.chess_game.promotion_choice = choice
                piece_name = self.PROMOTION_NAMES.get(choice, "UNKNOWN")
                self.serial_handler.display_text("SELECTED", piece_name)
                return True
        return False

    def handle_main_action_button(self):
        """Process the main action button (Now using B0/B2 for turns)"""
        if self.chess_game.promotion_pending:
            if self.chess_game.promotion_choice:
                success = self.chess_game.finalize_promotion(self.chess_game.promotion_choice)
                if success:
                    piece_name = self.PROMOTION_NAMES.get(self.chess_game.promotion_choice, "UNKNOWN")
                    self.serial_handler.display_text("PROMOTED TO", piece_name)
                    move = self.chess_game.board.peek().uci()
                    self.serial_handler.display_text("MOVE MADE", move)
                else:
                    self.serial_handler.display_text("INVALID", "PROMOTION")
                self.chess_game.promotion_choice = None
            else:
                self.serial_handler.display_text("SELECT", "PROMOTION!")
                self.serial_handler.display_text("USE BTNS", "4-7")
        else:

            result = self.chess_game.push_move()
            if result == "promotion_needed":
                self.serial_handler.display_text("CHOOSE PROMOTION", "USE BTNS 4-7")
            elif result:
                move = self.chess_game.board.peek().uci()
                self.serial_handler.display_text("MOVE MADE", move)
            else:
                self.serial_handler.display_text("INVALID MOVE", "TRY AGAIN")