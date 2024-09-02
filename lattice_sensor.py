"""
import serial
import time
from signal import pause
from gpiozero import Button, OutputDevice

rows=[2,3,4]
cols=[22,27,17,]
rows=[OutputDevice(pin, active_high=True, initial_value=False) for pin in rows]
columns=[Button(pin, pull_up=True) for pin in cols]

matrix=[[False for _ in range(3)] for _ in range(3)]
"""


def scan_matrix():
    """
    for i,row in enumerate(rows):
        row.on()
        for j,column in enumerate(columns):
            if column.is_pressed:
                matrix[i][j]=True
            else:
                matrix[i][j]=False
            print(matrix[i][j])
        row.off()
        time.sleep(1)
    return matrix

    scan_matrix()
    for row in matrix:
        print(row)
    """
    return None

