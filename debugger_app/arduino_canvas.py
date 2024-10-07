from .canvas import Canvas
from .ui_settings import *

class ArduinoCanvas(Canvas):
    def __init__(self, middle_frame, prev_canvas=None):
        super().__init__(ARDUINO_CID, middle_frame, prev_canvas=prev_canvas)

        # The string that will be displayed on the canvas
        self.logs = "Arduino serial logs"

    def draw(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing

        self.canvas.create_text(200, 200, text= self.logs, fill="black", font=font_style)

        self.updated = False
