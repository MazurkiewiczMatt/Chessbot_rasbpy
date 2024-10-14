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

        # Set the dimensions for the layout
        column_x_start = 25  # Starting x position for task names and values
        chart_x_start = 150  # Starting x position for the bars
        chart_y_start = 175  # Starting y position for the bars
        bar_height = 25  # Height of each bar
        spacing = 15  # Space between bars
        max_bar_width = 200  # Max width of the bars (adjust to fit your canvas size)

        # Calculate maximum task time for scaling the bars
        max_time = max(self.current_info['task_times_average'].values()) if self.current_info[
            'task_times_average'] else 1

        # Loop through the tasks and draw the task names, values, and bars
        for i, (task_name, avg_time) in enumerate(self.current_info['task_times_average'].items()):
            # Calculate bar width based on task time
            bar_width = (avg_time / max_time) * max_bar_width  # Scale bar width dynamically

            # Draw the task name and average time on the left side
            self.canvas.create_text(column_x_start,
                                    chart_y_start + i * (bar_height + spacing) + bar_height / 2,
                                    anchor="w",
                                    text=f"{task_name}: {avg_time:.2f} ms",
                                    fill="black", font=large_font_style)

            # Draw the bar on the right side of the column
            self.canvas.create_rectangle(chart_x_start,
                                         chart_y_start + i * (bar_height + spacing),
                                         chart_x_start + bar_width,
                                         chart_y_start + i * (bar_height + spacing) + bar_height,
                                         fill="blue")

        # Draw FPS and frame time info above the chart
        all_task_info = f"FPS: {self.current_info['average_fps']:.2f}\nFrame Time: {self.current_info['average_frame_time_ms']:.2f} ms"
        self.canvas.create_text(200, 100, text="PERFORMANCE ANALYSIS\n\n" + all_task_info, fill="black",
                                font=large_font_style)

        self.updated = False

    def update(self):
        if self.new_info != self.current_info and self.new_info is not None:
            self.current_info = self.new_info
            self.updated = True
        super().update()
