import tkinter as tk
import time

from .ui_settings import *

class MenuWidget:
    def __init__(self, bottom_frame):
        self.button_names = {
            0: GRID_CID, 1: PERFORMANCE_CID, 2: ARDUINO_CID, 3: LOGS_CID,
        }

        self.selected_canvas = GRID_CID

        # Array of buttons representing grid cells (single row)
        self.button_grid = []
        for i in range(len(self.button_names)):
            button = tk.Button(bottom_frame, text=self.button_names[i],
                               width=12, height=1, bg='snow2', fg='black', font=font_style,
                               command=self.set_canvas(self.button_names[i]))
            button.grid(row=0, column=i)
            self.button_grid.append(button)

        self.updated = False

    def set_canvas(self, canvas_name):
        def set_function():
            self.selected_canvas = canvas_name
        return set_function

    def draw(self):
        self.updated = False

    def update(self):
        if self.updated:
            self.draw()
        self.updated = False