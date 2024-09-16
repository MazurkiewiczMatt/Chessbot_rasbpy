import tkinter as tk

from .ui_settings import *

class Buttons:
    def __init__(self, bottom_frame):
        self.button_names = {
            0: "P1 1", 1: "P1 2", 2: "P2 1", 3: "P2 2",
            4: "UI 1", 5: "UI 2", 6: "UI 3", 7: "UI 4",
        }

        # Array of buttons representing grid cells (single row)
        self.button_grid = []
        for i in range(8):
            button = tk.Button(bottom_frame, text=self.button_names[i],
                               width=5, height=2, bg='snow2', fg='black', font=font_style)
            button.grid(row=0, column=i)
            self.button_grid.append(button)

        self.updated = False

    def set_button_active(self, index):
        if 0 <= index < len(self.button_grid):
            self.button_grid[index].config(bg='green')
        self.updated = True

    def set_button_not_active(self, index):
        if 0 <= index < len(self.button_grid):
            self.button_grid[index].config(bg='snow2')
        self.updated = True

    def draw(self):
        self.updated = False

    def update(self):

        if self.updated:
            self.draw()
        self.updated = False