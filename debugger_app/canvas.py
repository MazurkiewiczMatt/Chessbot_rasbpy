import tkinter as tk

from .ui_settings import *

class Canvas:
    def __init__(self, canvas_type, middle_frame):
        self.canvas_type = canvas_type
        self.updated = False
        self.canvas = tk.Canvas(middle_frame, width=400, height=400, bg=frame_color)
        self.canvas.pack(expand=True)

    def update(self):
        if self.updated:
            self.draw()
        self.updated = False

    def draw(self):
        raise NotImplementedError
