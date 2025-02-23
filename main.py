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
PROMOTION_MAP = {
    4: chess.QUEEN,  # UI 1
    5: chess.ROOK,  # UI 2
    6: chess.BISHOP,  # UI 3
    7: chess.KNIGHT  # UI 4
}
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
    if lattice_updated:
        chess_game.update_from_sensor(lattice_reading)
        chessboard_state_correct = chess_game.is_state_correct()

        # Update Arduino display
        if not chess_game.game_started:
            serial_handler.display_text("GAME NOT", "STARTED")
        elif chessboard_state_correct:
            serial_handler.display_text("GOOD TO GO", ":)")
        else:
            serial_handler.display_text("MAKE A", "MOVE")


    if buttons_updated:
        for i, pressed in enumerate(buttons_reading):
            if pressed and i in PROMOTION_MAP:

                chess_game.promotion_choice = PROMOTION_MAP[i]
                serial_handler.display_text("This is:",PROMOTION_MAP[i])
        # Check for pressed buttons and send messages
        if buttons_reading[0]:
            if chess_game.promotion_pending:
                if chess_game.promotion_choice:
                    success = chess_game.finalize_promotion(chess_game.promotion_choice)
                    if success:
                        piece_name = {
                            QUEEN: "QUEEN",
                            ROOK: "ROOK",
                            BISHOP: "BISHOP",
                            KNIGHT: "KNIGHT"
                        }[chess_game.promotion_choice]
                        serial_handler.display_text("PROMOTED TO", piece_name)
                        move = chess_game.board.peek().uci()
                        serial_handler.display_text("MOVE MADE", move, delay=2000)
                    else:
                        serial_handler.display_text("INVALID", "PROMOTION")
                    chess_game.promotion_choice = None
                else:
                    serial_handler.display_text("SELECT", "PROMOTION!")
                    serial_handler.display_text("USE UI", "BUTTONS 1-4")
            else:
                result = chess_game.push_move()
                if result == "promotion_needed":
                    serial_handler.display_text("CHOOSE", "PROMOTION")
                elif result:
                    serial_handler.display_text("MOVE MADE",
                                                f"{chess_game.board.peek().uci()}")
                else:
                    serial_handler.display_text("INVALID", "MOVE")    # Gameplay
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

    if buttons_updated:
        # Check for pressed buttons and send messages
        for i, button_reading in enumerate(buttons_reading, start=1):
            if button_reading:
                serial_handler.send_message(f"B{i}")
                serial_handler.display_text(f"Button B{i} ", "is ON")

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
