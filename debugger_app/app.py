import tkinter as tk

from .buttons import Buttons
from .grid import Grid
from .performance import Performance
from .info_widget import InfoWidget
from .menu_widget import MenuWidget
from .ui_settings import *


class DebuggerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Debugger")
        self.root.geometry("720x600")
        self.root.configure(background='dark slate gray')

        self.set_up_frames()

        self.info_widget = InfoWidget(self.top_frame)
        self.menu_frame = MenuWidget(self.menu_frame)
        self.canvas = Grid(self.middle_frame)
        self.buttons = Buttons(self.bottom_frame)

        self.draw()


    def set_up_frames(self):
        # Top Frame for FPS info
        self.top_frame = tk.Frame(self.root)
        self.top_frame.config(bg=frame_color)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=padding_y)

        # Menu frame
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.config(bg=bg_color)
        self.menu_frame.pack(side=tk.TOP, pady=menu_padding_y)

        # Main frame to hold the canvas and the side frames
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # Left frame
        self.left_frame = tk.Frame(self.main_frame, width=100, bg=bg_color)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Right frame
        self.right_frame = tk.Frame(self.main_frame, width=100, bg=bg_color)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Middle frame for the canvas
        self.middle_frame = tk.Frame(self.main_frame)
        self.middle_frame.config(bg=bg_color)
        self.middle_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Bottom Frame for buttons (on/off states)
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.config(bg=frame_color)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=padding_y)

    def set_connection(self, connected):
        self.info_widget.set_connection(connected)

    def set_button_active(self, index):
        self.buttons.set_button_active(index)

    def set_button_not_active(self, index):
        self.buttons.set_button_not_active(index)

    def set_task(self, task_name):
        self.info_widget.set_task(task_name)

    def draw(self):
        self.canvas.draw()
        self.info_widget.draw()
        self.buttons.draw()

    def update_grid(self, new_grid):
        if self.canvas.canvas_type == GRID_CID:
            self.canvas.update_grid(new_grid)

    def calculate_metrics(self):
        self.info_widget.calculate_metrics()

    def update(self):

        if self.menu_frame.selected_canvas != self.canvas.canvas_type:
            if self.menu_frame.selected_canvas == GRID_CID:
                self.canvas = Grid(self.middle_frame, prev_canvas=self.canvas.canvas)
            elif self.menu_frame.selected_canvas == PERFORMANCE_CID:
                self.canvas = Performance(self.middle_frame, prev_canvas=self.canvas.canvas)
            self.canvas.updated = True
            self.menu_frame.selected_canvas = self.canvas.canvas_type

        if self.canvas.canvas_type == PERFORMANCE_CID:
            if self.canvas.all_task_info != self.info_widget.all_task_info:
                self.canvas.all_task_info = self.info_widget.all_task_info
                self.canvas.updated = True

        self.info_widget.update()
        self.canvas.update()
        self.buttons.update()

        self.root.update_idletasks()
        self.root.update()
