import tkinter as tk
import time

from .ui_settings import *

class InfoWidget:
    def __init__(self, top_frame):
        self.info_widget = tk.Text(top_frame, height=4, width=80, bg=frame_color, bd=0, highlightthickness=0)
        self.info_widget.pack()
        self.info_widget.tag_configure("green", foreground="green")
        self.info_widget.tag_configure("red", foreground="red")
        # Initialize frame counting and timing
        self.frame_count = 0
        self.start_time = time.time()
        self.average_fps = 0
        self.average_frame_time_ms = 0
        self.updated = False
        # Task timing tracking
        self.tasks_times_average = {}
        self.task_times = {}
        self.task_start_time = None
        self.current_task_name = None

        self.connected_to_Arduino = False

    def set_connection(self, connected):
        self.connected_to_Arduino = connected
        self.updated = True

    def set_task(self, task_name):
        if self.current_task_name is not None:
            # End the previous task
            task_end_time = time.time()
            task_duration = (task_end_time - self.task_start_time) * 1000  # Convert to milliseconds
            if self.current_task_name not in self.task_times:
                self.task_times[self.current_task_name] = []
            self.task_times[self.current_task_name].append(task_duration)

        # Start timing for the new task
        self.current_task_name = task_name
        self.task_start_time = time.time()

    def draw(self):

        # Set the Text widget to be read-only
        self.info_widget.config(state="normal")

        # Clear the current content of the Text widget
        self.info_widget.delete('1.0', tk.END)

        # Insert FPS and Frame Time text
        title = f"Chessbot Raspberry Pi software\n"
        self.info_widget.insert("end", title)

        # Add Arduino connection status with color
        arduino_status = "connected" if self.connected_to_Arduino else "not connected"
        arduino_tag = "green" if self.connected_to_Arduino else "red"
        self.info_widget.insert("end", "Arduino ", arduino_tag)
        self.info_widget.insert("end", f"{arduino_status}", arduino_tag)

        self.info_widget.insert("end", "\n")

        # Insert FPS and Frame Time text
        fps_text = f"FPS: {self.average_fps:.2f}, Frame Time: {self.average_frame_time_ms:.2f} ms\n"
        self.info_widget.insert("end", fps_text)

        # Add task breakdown
        task_info_strings = []
        for task_name, avg_time in self.tasks_times_average.items():
            task_info_strings.append(f"{task_name}: {avg_time:.2f} ms")
        all_task_info = " | ".join(task_info_strings)
        self.info_widget.insert("end", all_task_info)

        # Apply center alignment to the entire content
        self.info_widget.tag_add("center", "1.0", "end")
        self.info_widget.tag_configure("center", justify="center")

        # Set the Text widget to be read-only
        self.info_widget.config(state="disabled")

        self.updated = False

    def calculate_metrics(self):
        # Calculate FPS
        elapsed_time = time.time() - self.start_time
        self.average_fps = self.frame_count / elapsed_time
        self.average_frame_time_ms = (elapsed_time / self.frame_count) * 1000

        # Calculate and store average durations for each task
        self.tasks_times_average = {task_name: sum(times) / len(times) for task_name, times in self.task_times.items()}

        # Reset the counters
        self.task_times = {}
        self.frame_count = 0
        self.start_time = time.time()

    def update(self):

        self.frame_count += 1
        elapsed_time = time.time() - self.start_time

        if elapsed_time >= 0.5:
            self.calculate_metrics()
            self.updated = True

        if self.updated:
            self.draw()
        self.updated = False
