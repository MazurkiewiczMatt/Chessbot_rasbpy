import tkinter as tk
import time


class DebuggerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Debugger")
        self.root.geometry("550x550")

        # Top Frame for FPS info
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        # display FPS info
        self.fps_label = tk.Label(self.top_frame, text="FPS: 0.00, Frame Time: 0.00 ms")
        self.fps_label.pack()

        # Middle Frame for the canvas grid
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(side=tk.TOP)

        # Create a canvas widget for the grid
        self.canvas = tk.Canvas(self.middle_frame, width=400, height=400)
        self.canvas.pack()

        # Define the size of each cell in the grid
        self.cell_size = 50

        # Initialize the grid
        self.grid = [[0 for _ in range(8)] for _ in range(8)]
        self.bg_grid = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]
        ]

        # Bottom Frame for buttons (on/off states)
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=10)

        self.button_names = {
            0: "P1 1", 1: "P1 2", 2: "P2 1", 3: "P2 2",
            4: "UI 1", 5: "UI 2", 6: "UI 3", 7: "UI 4",
        }

        # Array of buttons representing grid cells (single row)
        self.button_grid = []
        for i in range(8):
            button = tk.Button(self.bottom_frame, text=self.button_names[i],
                               width=5, height=2, bg='gray', fg='black')
            button.grid(row=0, column=i)
            self.button_grid.append(button)

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

        self.draw()

    def set_connection(self, connected):
        self.connected_to_Arduino = connected
        self.updated = True

    def set_button_active(self, index):
        if 0 <= index < len(self.button_grid):
            self.button_grid[index].config(bg='green')
        self.updated = True

    def set_button_not_active(self, index):
        if 0 <= index < len(self.button_grid):
            self.button_grid[index].config(bg='gray')
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
        self.canvas.delete("all")  # Clear the canvas before redrawing
        for i in range(8):
            for j in range(8):
                if self.grid[j][7-i] == 1:
                    color = "green"
                elif self.bg_grid[j][7-i] == 1:
                    color = "gray"
                else:
                    color = "white"
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                             (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                                             fill=color)
        display_str = f"FPS: {self.average_fps:.2f}, Frame Time: {self.average_frame_time_ms:.2f} ms"
        if self.connected_to_Arduino:
            display_str += "\n Arduino connected | "
        else:
            display_str += "\n Arduino not connected | "
        display_str += "Task breakdown: \n"
        for task_name, avg_time in self.tasks_times_average.items():
            display_str += f"{task_name}: {avg_time:.2f} ms\t"
        self.fps_label.config(text=display_str)


    def update_grid(self, new_grid):
        self.grid = new_grid
        self.updated = True

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

        self.root.update_idletasks()
        self.root.update()

