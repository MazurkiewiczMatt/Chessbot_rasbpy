import tkinter as tk
import time


class DebuggerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Debugger")
        self.root.geometry("400x500")  # Adjust the height for better layout

        # Top Frame for FPS info
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Create a Label to display FPS info
        self.fps_label = tk.Label(self.top_frame, text="FPS: 0.00, Frame Time: 0.00 ms")
        self.fps_label.pack()

        # Middle Frame for the canvas grid
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(side=tk.TOP)

        # Create a canvas widget for the grid
        self.canvas = tk.Canvas(self.middle_frame, width=400, height=400)
        self.canvas.pack()

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

        # Bottom Frame for buttons (on/off states)
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=10)

        self.button_names = {
            0: "Start", 1: "Stop", 2: "Pause", 3: "Resume",
            4: "Reset", 5: "Save", 6: "Load", 7: "Exit"
        }

        # Array of buttons representing grid cells (single row)
        self.button_grid = []
        for i in range(8):
            button = tk.Button(self.bottom_frame, text=self.button_names[i],
                               width=5, height=2, bg='gray', fg='black')
            button.grid(row=0, column=i)
            self.button_grid.append(button)

        # Initialize frame counting and timing
        self.frame_count = 0
        self.start_time = time.time()
        self.average_fps = 0
        self.average_frame_time_ms = 0
        self.updated = False

        self.draw()

    def set_button_active(self, index):
        if 0 <= index < len(self.button_grid):
            self.button_grid[index].config(bg='green')
        self.updated = True

    def set_button_not_active(self, index):
        if 0 <= index < len(self.button_grid):
            self.button_grid[index].config(bg='gray')
        self.updated = True

    def draw(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] == 1:
                    color = "green"
                elif self.bg_grid[i][j] == 1:
                    color = "gray"
                else:
                    color = "white"
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                             (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                                             fill=color)

        self.fps_label.config(text=f"FPS: {self.average_fps:.2f}, Frame Time: {self.average_frame_time_ms:.2f} ms")

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

        self.root.update_idletasks()
        self.root.update()

