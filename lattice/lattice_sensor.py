import time


class LatticeSensor:
    def __init__(self, dummy=False):
        self.dummy = dummy
        self.rows_pins = [9, 11, 0, 5, 6, 13, 19, 26]
        self.cols_pins = [10, 22, 27, 17, 12, 16, 20, 21]

        if not dummy:
            from gpiozero import Button, OutputDevice
            self.rows = [OutputDevice(pin, active_high=True, initial_value=False) for pin in self.rows_pins]
            self.columns = [Button(pin, pull_up=False) for pin in self.cols_pins]
        else:
            self.rows = [None for _ in self.rows_pins]
            self.columns = [None for _ in self.cols_pins]

        self.matrix = [[False for _ in range(len(self.columns))] for _ in range(len(self.rows))]

    def sense(self):
        if not self.dummy:
            for i, row in enumerate(self.rows):
                row.on()
                for j, column in enumerate(self.columns):
                    self.matrix[i][j] = int(column.is_pressed)
                row.off()
                time.sleep(0.0025)

        return self.matrix
