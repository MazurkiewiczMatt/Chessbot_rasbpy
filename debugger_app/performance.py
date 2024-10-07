from .canvas import Canvas
from .ui_settings import *

class Performance(Canvas):
    def __init__(self, middle_frame, prev_canvas=None):
        super().__init__(PERFORMANCE_CID, middle_frame, prev_canvas=prev_canvas)

        # The string that will be displayed on the canvas
        self.all_task_info = "Performance analysis initialized"

    def draw(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing

        # Draw the all_task_info string in the middle of the canvas
        self.canvas.create_text(200, 200, text="PERFORMANCE ANALYSIS \n\n" + self.all_task_info, fill="black", font=large_font_style)

        self.updated = False
