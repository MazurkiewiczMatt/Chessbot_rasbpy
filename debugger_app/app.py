import tkinter as tk
import time


class DebuggerApp:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Debugger")
        self.root.geometry("400x400")

        # Create a canvas widget
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        # Create a label to display FPS
        self.fps_label = tk.Label(self.root, text="FPS: 0.00")
        self.fps_label.pack()

        # Define the size of each cell in the grid
        self.cell_size = 50

        # Initialize the grid
        self.grid = [[0 for _ in range(8)] for _ in range(8)]
        self.bg_grid = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]
        ]

        # Initialize frame counting and timing
        self.frame_count = 0
        self.start_time = time.time()
        self.average_fps = 0
        self.average_frame_time_ms = 0
            
        self.updated = False

        self.draw()

    def draw(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] == 1:
                    color = "black"
                elif self.bg_grid[i][j] == 1:
                    color = "gray"
                else:
                    color = "white"
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                             (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                                             fill=color)
        self.fps_label.config(text=f"FPS: {self.average_fps:.2f}, Frame Time: {self.average_frame_time_ms:.2f} ms")

        self.root.update_idletasks()
        self.root.update()

    def update_grid(self, new_grid):
        self.grid = new_grid
        self.updated = True

    def update(self):

        self.frame_count += 1
        elapsed_time = time.time() - self.start_time

        if elapsed_time >= 0.1:  # Refresh every 0.1 seconds
            self.average_fps = self.frame_count / elapsed_time
            self.average_frame_time_ms = (elapsed_time / self.frame_count) * 1000
            # Reset the counters
            self.frame_count = 0
            self.start_time = time.time()
            self.updated = True

        if self.updated:
            self.draw()
            self.updated = False

