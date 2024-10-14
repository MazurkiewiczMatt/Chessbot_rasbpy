from .canvas import Canvas
from .ui_settings import *

class Grid(Canvas):
    def __init__(self, middle_frame, prev_canvas=None):

        super().__init__(GRID_CID, middle_frame, prev_canvas=prev_canvas)

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

        self.grid_colors = {
            "detected": "green",
            "black": "gray",
            "white": "white"
        }

    def draw(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing
        for i in range(8):
            for j in range(8):
                if self.grid[j][7 - i] == 1 and self.grid_colors["detected"] is not None:
                    color = self.grid_colors["detected"]
                elif self.bg_grid[j][7 - i] == 1:
                    color = self.grid_colors["black"]
                else:
                    color = self.grid_colors["white"]
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                             (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                                             fill=color)
        self.updated = False

    def update_grid(self, new_grid):
        self.grid = new_grid
        self.updated = True

