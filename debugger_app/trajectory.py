from .canvas import Canvas
from .ui_settings import *

class Trajectory(Canvas):
    def __init__(self, middle_frame, prev_canvas=None):
        super().__init__(TRAJECTORY_CID, middle_frame, prev_canvas=prev_canvas)


    def draw(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing

        self.updated = False
