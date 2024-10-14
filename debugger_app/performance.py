from .canvas import Canvas
from .ui_settings import *

class Performance(Canvas):
    def __init__(self, middle_frame, prev_canvas=None):
        super().__init__(PERFORMANCE_CID, middle_frame, prev_canvas=prev_canvas)

        # The string that will be displayed on the canvas
        self.text = "Performance analysis initialized"
        self.current_info = None
        self.new_info = None

    def draw(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing

        task_info_strings = []
        for task_name, avg_time in self.current_info['task_times_average'].items():
            task_info_strings.append(f"{task_name}: {avg_time:.2f} ms")
        all_task_info = f"FPS: {self.current_info["average_fps"]:.2f} \n \nFrame Time: {self.current_info["average_frame_time_ms"]:.2f} ms\nBreakdown: \n  "
        all_task_info += " \n  ".join(task_info_strings)

        # Draw the all_task_info string in the middle of the canvas
        self.canvas.create_text(200, 200, text="PERFORMANCE ANALYSIS \n\n" + all_task_info, fill="black", font=large_font_style)

        self.updated = False


    def update(self):
        if self.new_info != self.current_info and self.new_info is not None:
            self.current_info = self.new_info
            self.updated = True
        super().update()
