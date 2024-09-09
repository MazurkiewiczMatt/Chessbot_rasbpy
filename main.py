from settings import *
from lattice import LatticeSensor
from debugger_app import DebuggerApp
from arduino_serial import SerialHandler
from buttons import ButtonSensors

running = True

print("The ChessBot's Raspberry Pi software has been launched!")

if DEBUG:
    app = DebuggerApp()

serial_handler = SerialHandler('/dev/ttyACM0', 115200, dummy=(DUMMY or ARDUINO_DUMMY))
button_pins = [14, 15, 18, 23, 24, 25, 8, 7]
button_sensors = ButtonSensors(button_pins, dummy=DUMMY)
last_buttons_reading = None
lattice_sensor = LatticeSensor(dummy=DUMMY)
last_lattice_reading = None

while running:

    # Process lattice
    if DEBUG:
        app.set_task("lattice")
    lattice_reading = lattice_sensor.sense()
    lattice_updated = lattice_reading != last_lattice_reading

    # Get button states
    if DEBUG:
        app.set_task("buttons")
    buttons_reading = button_sensors.sense()
    buttons_updated = buttons_reading != last_buttons_reading


    # Serial communication with Arduino
    if DEBUG:
        app.set_task("serial")
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
            for i, button_reading in enumerate(buttons_reading, start=1):
                if button_reading:
                    app.set_button_active(i)
                else:
                    app.set_button_not_active(i)
        app.update()

    # Update last reading
    last_lattice_reading = lattice_reading
    last_buttons_reading = buttons_reading
