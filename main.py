from settings import *
from lattice import LatticeSensor
from debugger_app import DebuggerApp
from debugger_app.arduino_canvas import ArduinoCanvas
from debugger_app.trajectory import Trajectory
from arduino_serial import SerialHandler
from buttons import ButtonSensors

running = True

print("The ChessBot's Raspberry Pi software has been launched!")

if DEBUG:
    app = DebuggerApp()

serial_handler = SerialHandler('/dev/ttyACM0', 9600, dummy=ARDUINO_DUMMY)
button_sensors = ButtonSensors(dummy=DUMMY)
last_buttons_reading = None
lattice_sensor = LatticeSensor(dummy=DUMMY)
last_lattice_reading = None

serial_handler.display_text("INITIATED v2", "")

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

                column=app.canvas.selected_square[0]
                row=app.canvas.selected_square[1]

                y1_cm = column * 4.5 + 6.75
                x1_cm = 15.75 - row * 4.5
                serial_handler.display_text(f"Col: {column},{row}",f"Row: {y1_cm},{x1_cm}")
                #serial_handler.send_motor_command(XXX)
                app.canvas.square_sent = True

    if buttons_updated:
        # Check for pressed buttons and send messages
        for i, button_reading in enumerate(buttons_reading, start=1):
            if button_reading:
                serial_handler.send_message(f"B{i}")

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
    last_lattice_reading = list(list(column) for column in lattice_reading)
    last_buttons_reading = list(buttons_reading)
