from .grid import Grid
from .ui_settings import *

class Trajectory(Grid):
    def __init__(self, middle_frame, prev_canvas=None):
        super().__init__(middle_frame, prev_canvas=prev_canvas)
        self.canvas_type = TRAJECTORY_CID
        self.grid_colors = {
            "detected": None,
            "black": "DarkOrange4",
            "white": "DarkOrange1"
        }
        self.selected_square = None  # To store the selected square coordinates

        # Bind the click event to the canvas
        self.canvas.bind("<Button-1>", self.on_click)
        self.show_canvas = False  # Will trigger unbinding

    def on_click(self, event):
        """Handles the click event and selects the square."""
        # Calculate the row and column based on the click coordinates
        row = event.y // self.cell_size
        col = event.x // self.cell_size

        # Check if the click is within the bounds of the grid
        if 0 <= row < 8 and 0 <= col < 8:
            self.selected_square = (col, row)
            self.updated = True
            self.draw()  # Redraw the grid with the selected square

    def draw(self):
        # Call the super class draw method to draw the grid
        super().draw()

        # Draw a red circle on the selected square if one is selected
        if self.selected_square:
            col, row = self.selected_square
            # Draw a red circle in the middle of the selected square
            x1 = col * self.cell_size + self.cell_size // 8
            y1 = row * self.cell_size + self.cell_size // 8
            x2 = (col + 1) * self.cell_size - self.cell_size // 8
            y2 = (row + 1) * self.cell_size - self.cell_size // 8

            self.canvas.create_oval(x1, y1, x2, y2, outline="white", width=3)

    def toggle_view(self):
        self.canvas.unbind("<Button-1>")