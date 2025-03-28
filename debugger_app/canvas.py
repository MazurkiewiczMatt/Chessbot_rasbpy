import tkinter as tk

from .ui_settings import *

class Canvas:
    def __init__(self, canvas_type, middle_frame, prev_canvas=None):
        self.canvas_type = canvas_type
        self.updated = False
        if prev_canvas is None:
            self.canvas = tk.Canvas(middle_frame, width=400, height=400, bg=frame_color)
            self.canvas.pack(expand=True)
        else:
            self.canvas = prev_canvas

        self.show_canvas = True

    def update(self):
        if self.updated:
            self.draw()
        self.updated = False

    def draw(self):
        raise NotImplementedError

    def toggle_view(self):
        if self.show_canvas:
            self.canvas.pack_forget()
        else:
            self.canvas.pack(expand=True)
        self.show_canvas = not self.show_canvas
