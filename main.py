from settings import *
from lattice import scan_matrix, GridApp

import time
import tkinter as tk

running = True

if DEBUG:
    # Variables for debugging

    frame_count = 0
    start_time = time.time()

    initial_grid = [
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0]
    ]
    root = tk.Tk()
    app = GridApp(root, initial_grid)

print("The ChessBot's raspberry Pi software has been launched!")
while running:

    # Process lattice
    lattice_reading = scan_matrix()
    if lattice_reading is not None:
        print("The state of the board has been updated!")
        print(lattice_reading)
        if DEBUG:
            app.update_grid(lattice_reading)
            root.update()

    # Update timers and do all other stuff

    if DEBUG:
        # Framerate monitoring
        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time >= DEBUG_INTERVAL:
            average_fps = frame_count / elapsed_time
            average_frame_time_ms = (elapsed_time / frame_count) * 1000
            print(f"Average framerate over the last {elapsed_time:.2f} seconds: {average_fps:.2f} FPS")
            print(f"Average time per frame: {average_frame_time_ms:.2f} ms")
            frame_count = 0
            start_time = time.time()
