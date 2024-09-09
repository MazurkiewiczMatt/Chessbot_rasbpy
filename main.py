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
    lattice_reading = lattice_sensor.sense()
    lattice_updated = lattice_reading != last_lattice_reading

    # Get button states
    buttons_reading = button_sensors.sense()
    buttons_updated = buttons_reading != last_buttons_reading

    if lattice_updated:
        if DEBUG:
            app.update_grid(lattice_reading)

    if buttons_updated:
        # Check for pressed buttons and send messages
        for i, button_reading in enumerate(buttons_reading, start=1):
            if button_reading:
                app.set_button_active(i)
                serial_handler.send_message(f"B{i}")
            else:
                app.set_button_not_active(i)

    # Update timers and do all other stuff
    if DEBUG:
        app.update()

    # Update last reading
    last_lattice_reading = lattice_reading
    last_buttons_reading = buttons_updated
