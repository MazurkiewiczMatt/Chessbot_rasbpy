from .grid import Grid
from .ui_settings import *

class Trajectory(Grid):
    def __init__(self, middle_frame, prev_canvas=None):
        super().__init__(middle_frame, prev_canvas=prev_canvas)
        self.canvas_type = TRAJECTORY_CID
        self.grid_colors = {
            "detected": None,
            "black": "green",
            "white": "yellow"
        }
