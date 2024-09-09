import tkinter as tk
import time

class DebuggerApp:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Debugger")
        self.root.geometry("200x200")

        # Create a canvas widget
        self.canvas = tk.Canvas(self.root, width=200, height=200)
        self.canvas.pack()

        # Create a label to display FPS
        self.fps_label = tk.Label(self.root, text="FPS: 0.00")
        self.fps_label.pack()

        # Define the size of each cell in the grid
        self.cell_size = 25

        # Initialize the grid
        self.grid = [[0 for _ in range(8)] for _ in range(8)]

        # Draw the initial grid
        self.draw_grid()

        # Initialize frame counting and timing
        self.frame_count = 0
        self.start_time = time.time()
        self.updated = False

    def draw_grid(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing
        for i in range(8):
            for j in range(8):
                color = "black" if self.grid[i][j] == 1 else "white"
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                             (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                                             fill=color)

    def update_grid(self, new_grid):
        self.grid = new_grid
        self.updated = True

    def update(self):

        self.frame_count += 1
        elapsed_time = time.time() - self.start_time

        if elapsed_time >= 0.1:  # Refresh every 0.1 seconds
            average_fps = self.frame_count / elapsed_time
            average_frame_time_ms = (elapsed_time / self.frame_count) * 1000
            self.fps_label.config(text=f"FPS: {average_fps:.2f}, Frame Time: {average_frame_time_ms:.2f} ms")

            # Reset the counters
            self.frame_count = 0
            self.start_time = time.time()
            self.updated = True

        if self.updated:
            self.draw()
            self.updated = False

    def draw(self):
        self.draw_grid()
        self.root.update_idletasks()
        self.root.update()
