from settings import *
from lattice import LatticeSensor
from debugger_app import DebuggerApp
from debugger_app.arduino_canvas import ArduinoCanvas
from debugger_app.trajectory import Trajectory
from arduino_serial import SerialHandler
from buttons import ButtonSensors
from chessboard import ChessGameSimulator
from gameplay import Gameplay
from robot_arms import RobotArmHandler
import chess
running = True

print("The ChessBot's Raspberry Pi software has been launched!")

if DEBUG:
    app = DebuggerApp()

# Hardware modules
serial_handler = SerialHandler('/dev/ttyACM0', 9600, dummy=ARDUINO_DUMMY)
button_sensors = ButtonSensors(dummy=DUMMY)
last_buttons_reading = None
lattice_sensor = LatticeSensor(dummy=DUMMY)
last_lattice_reading = None

# Software modules
chessboard_state_correct = None
gameplay = Gameplay()
robot_arm = RobotArmHandler()
chess_game = ChessGameSimulator()
#serial_handler.display_text("INITIATED", "NOTHING")

# Update PROMOTION_MAP in main.py
PROMOTION_MAP = {
    4: chess.BISHOP,  # B4 - Bishop
    5: chess.KNIGHT,  # B5 - Knight
    6: chess.QUEEN,   # B6 - Queen
    7: chess.ROOK     # B7 - Rook
}

PROMOTION_NAMES = {
    chess.QUEEN: "QUEEN",
    chess.ROOK: "ROOK",
    chess.BISHOP: "BISHOP",
    chess.KNIGHT: "KNIGHT"
}
def display_turn_status():
    """Update display with current turn information"""
    if chess_game.current_turn == chess.WHITE:
        serial_handler.display_text("WHITE'S TURN", "PRESS B0 TO END")
    else:
        serial_handler.display_text("BLACK'S TURN", "PRESS B2 TO END")
def handle_promotion_selection(buttons_reading):
    """Process promotion button selections and update display"""
    for btn_idx, pressed in enumerate(buttons_reading):
        if pressed and btn_idx in PROMOTION_MAP:
            choice = PROMOTION_MAP[btn_idx]
            chess_game.promotion_choice = choice
            piece_name = PROMOTION_NAMES.get(choice, "UNKNOWN")
            serial_handler.display_text("SELECTED", piece_name)
            return True
    return False


# Update handle_main_action_button in main.py:
def handle_main_action_button(chess_game):
    """Process the main action button (Now using B0/B2 for turns)"""
    if chess_game.promotion_pending:
        if chess_game.promotion_choice:
            success = chess_game.finalize_promotion(chess_game.promotion_choice)
            if success:
                piece_name = PROMOTION_NAMES.get(chess_game.promotion_choice, "UNKNOWN")
                serial_handler.display_text("PROMOTED TO", piece_name)
                move = chess_game.board.peek().uci()
                serial_handler.display_text("MOVE MADE", move)
            else:
                serial_handler.display_text("INVALID", "PROMOTION")
            chess_game.promotion_choice = None
        else:
            serial_handler.display_text("SELECT", "PROMOTION!")
            serial_handler.display_text("USE BTNS", "4-7")
    else:
        # Restrict moves to current player's turn
        if chess_game.board.turn != chess_game.current_turn:
            serial_handler.display_text("WRONG TURN", "USE B0/B2")
            return

        result = chess_game.push_move()
        if result == "promotion_needed":
            serial_handler.display_text("CHOOSE", "PROMOTION")
            serial_handler.display_text("USE BTNS", "4-7")
        elif result:
            serial_handler.display_text("MOVE MADE", f"{chess_game.board.peek().uci()}")
        else:
            serial_handler.display_text("INVALID", "MOVE")



while running:

    # Process lattice
    if DEBUG:
        app.set_task("lattice")
    lattice_reading = lattice_sensor.sense()
    lattice_updated = (lattice_reading != last_lattice_reading)

    # Get button states
    if DEBUG:
        app.set_task("buttons")
    buttons_reading = button_sensors.sense()
    buttons_updated = buttons_reading != last_buttons_reading

    # Gameplay
    if DEBUG:
        app.set_task("chessboard")

    # Replace the lattice_updated block in main.py's while loop:
    if lattice_updated:
        chess_game.update_from_sensor(lattice_reading)
        chessboard_state_correct = chess_game.is_state_correct()

        # Handle game setup assistance
        if not chess_game.game_started:
            missing = chess_game.get_missing_start_pieces(lattice_reading)

            # Replace the missing pieces display logic with:
            if len(missing) > 0 and len(missing) <= 4:
                # Split missing squares into chunks of 2
                chunks = [missing[i:i + 2] for i in range(0, len(missing), 2)]
                # Format with proper spacing
                line1 = " ".join(chunks[0]).ljust(14) if len(chunks) > 0 else ""
                line2 = " ".join(chunks[1]).ljust(14) if len(chunks) > 1 else ""
                serial_handler.display_text(line1[:14], line2[:14])
            elif len(missing) > 4:
                serial_handler.display_text("MISSING", f"{len(missing)} PIECES")
            else:
                serial_handler.display_text("READY TO START", "PRESS B0/B2")
        else:
            # Existing game state display
            if chessboard_state_correct:
                serial_handler.display_text("GOOD TO GO", ":)")
            else:
                serial_handler.display_text("MAKE A", "MOVE")

    # Replace the buttons_updated block in main.py's while loop:
    # Replace the existing button handling code with:

    if buttons_updated:
        # Handle turn completion buttons
        if buttons_reading[0]:  # B0 - White's turn complete
            if chess_game.current_turn == chess.WHITE and chess_game.board.turn == chess.WHITE:
                chess_game.current_turn = chess.BLACK
                serial_handler.display_text("TURN ENDED", "BLACK'S TURN")
            else:
                serial_handler.display_text("CAN'T END TURN", "MAKE WHITE MOVE")

        if buttons_reading[2]:  # B2 - Black's turn complete
            if chess_game.current_turn == chess.BLACK and chess_game.board.turn == chess.BLACK:
                chess_game.current_turn = chess.WHITE
                serial_handler.display_text("TURN ENDED", "WHITE'S TURN")
            else:
                serial_handler.display_text("CAN'T END TURN", "MAKE BLACK MOVE")

        # Process promotion selection buttons (4-7)
        promotion_selected = handle_promotion_selection(buttons_reading)

        # Handle reserved player buttons (B1 and B3)
        if any(buttons_reading[i] for i in [1, 3]) and not promotion_selected:
            serial_handler.display_text("BUTTON RESERVED", "FOR FUTURE USE")

        # Update turn display after any button interaction
        display_turn_status()

    if DEBUG:
        app.set_task("gameplay")
    # here call gameplay, with any if statement, any method any parameters
    gameplay.update(None)
    action = gameplay.get_action()
    if action is not None:
        robot_arm.scheduled_movements(action)

    if DEBUG:
        app.set_task("robot_arm")
    # here call robot_arm, with any if statement, any method any parameters
    arduino_robot_arm_instruction = robot_arm.update()


    # Serial communication with Arduino
    if DEBUG:
        app.set_task("serial")
        app.set_connection(serial_handler.ping())
        app.update_ardunio_logs(serial_handler.logs)
        if isinstance(app.canvas, ArduinoCanvas):
            if app.canvas.message_to_be_sent is not None:
                serial_handler.send_message(app.canvas.message_to_be_sent)
                app.canvas.message_to_be_sent = None
                serial_handler.receive_message()
        elif isinstance(app.canvas, Trajectory):
            if not(app.canvas.square_sent) and app.canvas.selected_square is not None:

                column = app.canvas.selected_square[0]
                row = app.canvas.selected_square[1]

                # serial_handler.send_motor_command(XXX)
                app.canvas.square_sent = True
    # If movement scheduled and can move, call motors here
    if arduino_robot_arm_instruction != "":
        serial_handler.send_message(arduino_robot_arm_instruction)

    # GUI
    if DEBUG:
        app.set_task("GUI")
        if lattice_updated:
            app.update_grid(lattice_reading)
        if buttons_updated:
            for i, button_reading in enumerate(buttons_reading):
                if button_reading:
                    app.set_button_active(i)
                else:
                    app.set_button_not_active(i)
        app.update()

    # Update last reading
    last_lattice_reading = [list(column) for column in lattice_reading]
    last_buttons_reading = list(buttons_reading)

    # Reset lattice reading after processing
    lattice_sensor.sense()
