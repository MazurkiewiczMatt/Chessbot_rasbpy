from settings import *
from lattice import LatticeSensor
from debugger_app import DebuggerApp
from arduino_serial import SerialHandler
from buttons import ButtonSensors

running = True

print("The ChessBot's Raspberry Pi software has been launched!")

if DEBUG:
    app = DebuggerApp()

serial_handler = SerialHandler('/dev/ttyACM0', 115200, dummy=DUMMY)
button_pins = [14, 15, 18, 23, 24, 25, 8, 7]
button_sensors = ButtonSensors(button_pins, serial_handler, dummy=DUMMY)
lattice_sensor = LatticeSensor(dummy=DUMMY)
last_reading = None

while running:

    # Process lattice
    lattice_reading = lattice_sensor.sense()
    lattice_updated = lattice_reading != last_reading

    if lattice_updated:
        if DEBUG:
            app.update_grid(lattice_reading)

    # Update timers and do all other stuff
    if DEBUG:
        app.update()

    # Update last reading
    last_reading = lattice_reading
