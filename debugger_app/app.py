import tkinter as tk
import time


class DebuggerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Debugger")
        self.root.geometry("720x576")
        self.root.configure(background='dark slate gray')

        padding_y = 12
        frame_color = "snow2"
        bg_color = 'dark slate gray'
        font_style = ("Helvetica", 10, "bold")

        # Top Frame for FPS info
        self.top_frame = tk.Frame(self.root)
        self.top_frame.config(bg=frame_color)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=padding_y)

        # display FPS info
        self.fps_label = tk.Label(self.top_frame, text="# INITIALIZING #")
        self.fps_label.config(font=font_style, bg=frame_color)
        self.fps_label.pack()

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

        # Create a canvas widget for the grid, centered in the middle frame
        self.canvas = tk.Canvas(self.middle_frame, width=400, height=400, bg=frame_color)
        self.canvas.pack(expand=True)

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
        self.bottom_frame.config(bg=frame_color)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=padding_y)

        self.button_names = {
            0: "P1 1", 1: "P1 2", 2: "P2 1", 3: "P2 2",
            4: "UI 1", 5: "UI 2", 6: "UI 3", 7: "UI 4",
        }


        # Array of buttons representing grid cells (single row)
        self.button_grid = []
        for i in range(8):
            button = tk.Button(self.bottom_frame, text=self.button_names[i],
                               width=5, height=2, bg='snow2', fg='black', font=font_style)
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
            self.button_grid[index].config(bg='snow2')
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
        self.draw_info_label()

    def draw_info_label(self):
        # Create the initial display string for FPS and Frame Time
        display_str = f"FPS: {self.average_fps:.2f}, Frame Time: {self.average_frame_time_ms:.2f} ms\n"

        # Add Arduino connection status
        arduino_status = "connected" if self.connected_to_Arduino else "not connected"
        display_str += f"Arduino {arduino_status} | "

        # Add task breakdown
        task_breakdown = "\nTask breakdown:\n" + "\t".join(
            f"{task_name}: {avg_time:.2f} ms" for task_name, avg_time in self.tasks_times_average.items()
        )

        # Update the label text
        self.fps_label.config(text=display_str + task_breakdown)

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

