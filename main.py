from lattice_sensor import scan_matrix
import time

print("The ChessBot's raspberry Pi software has been launched!")

debug = True

# Variables for debugging
frame_count = 0
start_time = time.time()

running = True

while running:

    # Process lattice
    lattice_reading = scan_matrix()
    if lattice_reading is not None:
        print("The state of the board has been updated!")
        print(lattice_reading)

    # Update timers and do all other stuff

    if debug:
        # Framerate monitoring
        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time >= 10.0:
            average_fps = frame_count / elapsed_time
            average_frame_time_ms = (elapsed_time / frame_count) * 1000
            print(f"Average framerate over the last {elapsed_time:.2f} seconds: {average_fps:.2f} FPS")
            print(f"Average time per frame: {average_frame_time_ms:.2f} ms")
            frame_count = 0
            start_time = time.time()
