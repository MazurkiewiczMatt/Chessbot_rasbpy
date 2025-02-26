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
# Add this import at the top with other imports
import chess
from chess import QUEEN, ROOK, BISHOP, KNIGHT
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
                serial_handler.display_text("MOVE MADE", move, delay=2000)
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
            if len(missing) > 0 and len(missing) <= 4:
                # Format missing squares for display
                line1 = " ".join(missing[:2]).ljust(16)
                line2 = " ".join(missing[2:4]).ljust(16)
                serial_handler.display_text(line1, line2)
            elif len(missing) > 4:
                serial_handler.display_text("TOO MANY PIECES", "MISSING")
            else:
                serial_handler.display_text("READY TO START", "PRESS B0/B2")
        else:
            # Existing game state display
            if chessboard_state_correct:
                serial_handler.display_text("GOOD TO GO", ":)")
            else:
                serial_handler.display_text("MAKE A", "MOVE")

    # Replace the buttons_updated block in main.py's while loop:
    if buttons_updated:
        # Process promotion buttons
        promotion_selected = handle_promotion_selection(buttons_reading)

        # Handle turn completion buttons
        if buttons_reading[0]:  # B0 - White's turn complete
            if chess_game.current_turn == chess.WHITE:
                chess_game.current_turn = chess.BLACK
                serial_handler.display_text("BLACK'S TURN", "PRESS B2")
            else:
                serial_handler.display_text("WRONG TURN", "WHITE'S TURN")

        if buttons_reading[2]:  # B2 - Black's turn complete
            if chess_game.current_turn == chess.BLACK:
                chess_game.current_turn = chess.WHITE
                serial_handler.display_text("WHITE'S TURN", "PRESS B0")
            else:
                serial_handler.display_text("WRONG TURN", "BLACK'S TURN")

        # Process main action button (now handled by B0/B2)
        # ... rest of button handling remains same

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
