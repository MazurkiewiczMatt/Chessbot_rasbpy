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

    if DEBUG:
        app.set_task("gameplay")
    if buttons_updated:
        # Handle turn completion buttons, promotion, etc., in the game logic
        gameplay.process_button_reading(buttons_reading)
    # here move robot
    #robot_arm.scheduled_movements(action)

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
