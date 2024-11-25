import serial
from datetime import datetime
import time

from settings import ARDUINO_PING_PERIOD


class SerialHandler:
    def __init__(self, port, baudrate, timeout=1.0, dummy=False):
        if not dummy:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            self.ser.reset_input_buffer()  # Reset the input buffer on initialization
        else:
            self.ser = None

        self.logs = ""
        self.last_ping = time.time()
        self.last_ping_response = None

    def send_message(self, message):
        if self.ser is not None:
            self.ser.write(message.encode('utf-8'))
            self.logs += datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ">>> " + message + "\n"

    def receive_message(self):
        if self.ser is not None:
            message = self.ser.readline().decode('utf-8').strip()
            self.logs += "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + message + "\n"
            return message
        return None

    def ping(self):
        if self.ser is not None:
            current_time = time.time()
            if (current_time - self.last_ping >= ARDUINO_PING_PERIOD) or self.last_ping_response is None:
                self.send_message("PING")
                self.last_ping_response = self.receive_message()
                self.last_ping = current_time
            return self.last_ping_response == "PONG"
        else:
            return False

    def display_text(self, txt1,txt2):
        if self.ser is not None:
            self.send_message(f"LCD {txt1}, {txt2}")
            response = self.receive_message()
            return response == "LCD SUCCESS"
        else:
            return False

    def send_motor_command(self, steps1, steps2):
        if self.ser is not None:
            self.ser.write(f"MOVE, {steps1}, {steps2}")
            response = self.receive_message()
            return "MOVE SUCCESS" in response
        else:
            return False
