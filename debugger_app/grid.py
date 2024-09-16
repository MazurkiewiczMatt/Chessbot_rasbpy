import tkinter as tk

from .ui_settings import *

class Grid:
    def __init__(self, middle_frame):

        # Create a canvas widget for the grid, centered in the middle frame
        self.canvas = tk.Canvas(middle_frame, width=400, height=400, bg=frame_color)
        self.canvas.pack(expand=True)

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

        self.updated = False

    def draw(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing
        for i in range(8):
            for j in range(8):
                if self.grid[j][7 - i] == 1:
                    color = "green"
                elif self.bg_grid[j][7 - i] == 1:
                    color = "gray"
                else:
                    color = "white"
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                             (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                                             fill=color)
        self.updated = False

    def update_grid(self, new_grid):
        self.grid = new_grid
        self.updated = True

    def update(self):

        if self.updated:
            self.draw()
        self.updated = False