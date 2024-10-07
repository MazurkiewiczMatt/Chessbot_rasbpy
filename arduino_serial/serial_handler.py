import serial
from datetime import datetime

class SerialHandler:
    def __init__(self, port, baudrate, timeout=1.0, dummy=False):
        if not dummy:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            self.ser.reset_input_buffer()  # Reset the input buffer on initialization
        else:
            self.ser = None

        self.logs = ""

    def send_message(self, message, log=True):
        if self.ser is not None:
            self.ser.write(message.encode('utf-8'))
            if log:
                self.logs += datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ">>> " + message + "\n"

    def receive_message(self, log=True):
        if self.ser is not None:
            message = self.ser.readline().decode('utf-8').strip()
            if log:
                self.logs += "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + message + "\n"
            return message
        return None

    def ping(self):
        if self.ser is not None:
            self.send_message("PING", log=False)
            response = self.receive_message(log=False)
            return response == "PONG"
        else:
            return False

    def display_text(self, txt):
        if self.ser is not None:
            self.send_message(f"LCD {txt}")
            response = self.receive_message()
            return response == "LCD SUCCESS"
        else:
            return False
