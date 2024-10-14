import tkinter as tk

from .canvas import Canvas
from .ui_settings import *

class ArduinoCanvas(Canvas):
    def __init__(self, middle_frame, prev_canvas=None):
        super().__init__(ARDUINO_CID, middle_frame, prev_canvas=prev_canvas)

        # Create a frame to hold the logs and input widgets
        self.container_frame = tk.Frame(middle_frame)

        self.container_frame.grid_rowconfigure(0, weight=1)  # Log Text takes up remaining space
        self.container_frame.grid_columnconfigure(0, weight=1)  # Makes widgets expand horizontally

        # Create a Text widget for logs with a Scrollbar
        self.log_text = tk.Text(self.container_frame, wrap=tk.WORD, font=font_style)
        self.log_scrollbar = tk.Scrollbar(self.container_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.log_scrollbar.set)

        # Use grid layout for better space allocation
        self.log_text.grid(row=0, column=0, sticky="nsew")  # Log Text in first row
        self.log_scrollbar.grid(row=0, column=1, sticky="ns")  # Scrollbar on the side of the Text widget

        # Create an Entry widget for text input
        self.input_entry = tk.Entry(self.container_frame, font=font_style)
        self.input_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5,
                              pady=5)  # Entry widget in the second row
        self.input_entry.bind("<Return>", self.send)

        self.message_to_be_sent = None

        self.toggle_view()

        # Initialize logs
        self.logs = "Arduino serial logs"
        self.display_logs()

    def send(self, trigger):
        message = self.input_entry.get()
        if message:
            self.message_to_be_sent = message
            self.input_entry.delete(0, tk.END)


    def display_logs(self):
        """
        Updates the logs in the Text widget, keeping the latest log at the bottom.
        """
        self.log_text.config(state=tk.NORMAL)  # Make the Text widget editable
        self.log_text.delete(1.0, tk.END)  # Clear the current logs
        self.log_text.insert(tk.END, self.logs)  # Insert new logs
        self.log_text.config(state=tk.DISABLED)  # Make the Text widget read-only
        self.log_text.yview(tk.END)  # Scroll to the bottom

    def toggle_view(self):
        if self.show_canvas:
            self.container_frame.pack(expand=True, fill=tk.BOTH)  # Show the logs and input
        else:
            self.container_frame.pack_forget()  # Hide logs and input
        super().toggle_view()


    def draw(self):
        self.display_logs()
        self.updated = False
