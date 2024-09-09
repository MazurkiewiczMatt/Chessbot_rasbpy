from settings import *
from lattice import scan_matrix
from debugger_app import DebuggerApp

running = True

print("The ChessBot's Raspberry Pi software has been launched!")

if DEBUG:
    app = DebuggerApp()

last_reading = None

while running:

    # Process lattice
    lattice_reading = scan_matrix()
    lattice_updated = lattice_reading != last_reading

    if lattice_updated:
        if DEBUG:
            app.update_grid(lattice_reading)

    # Update timers and do all other stuff
    if DEBUG:
        app.update()

    # Update last reading
    last_reading = lattice_reading
