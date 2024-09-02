import time
from gpiozero import Button, OutputDevice

rows_pins = [26, 19, 13, 6, 5, 0, 11, 9]
cols_pins = [10, 22, 27, 17, 12, 16, 20, 21]
rows = [OutputDevice(pin, active_high=True, initial_value=False) for pin in rows_pins]
columns = [Button(pin, pull_up=True) for pin in cols_pins]
matrix=[[False for _ in range(len(columns))] for _ in range(len(rows))]

def scan_matrix():
    for i,row in enumerate(rows):
        row.on()
        for j,column in enumerate(columns):
            matrix[i][j] = column.is_pressed
            time.sleep(0.0005)
        row.off()
        time.sleep(0.01)
    return matrix

