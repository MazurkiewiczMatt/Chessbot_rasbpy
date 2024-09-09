import serial

class SerialHandler:
    def __init__(self, port, baudrate, timeout=1.0, dummy=False):
        if not dummy:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            self.ser.reset_input_buffer()  # Reset the input buffer on initialization
        else:
            self.ser = None

    def send_message(self, message):
        if self.ser is not None:
            self.ser.write(message.encode('utf-8'))

    def receive_message(self):
        if self.ser is not None:
            return self.ser.readline().decode('utf-8').strip()
        return None

    def ping(self):
        self.send_message("PING")
        response = self.receive_message()
        if response == "PONG":
            print("Ping successful")
        else:
            print("Ping failed or no response")
