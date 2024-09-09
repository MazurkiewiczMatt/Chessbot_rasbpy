import time
import serial
from signal import pause
from gpiozero import Button, OutputDevice
ser=serial.Serial('/dev/ttyACM0',115200, timeout=1.0)
time.sleep(3)

b1=Button(14)
b2=Button(15)
b3=Button(18)
b4=Button(23)
b5=Button(24)
b6=Button(25)
b7=Button(8)
b8=Button(7)

ser.rester_input_buffer()

def button1_pressed():
    print("BUTTON 1")
    ser.write("B1".encode('utf-8'))
def button2_pressed():
    print("BUTTON 2")
    ser.write("B2".encode('utf-8'))
def button3_pressed():
    print("BUTTON 3")
    ser.write("B3".encode('utf-8'))
def button4_pressed():
    print("BUTTON 4")
    ser.write("B4".encode('utf-8'))
def button5_pressed():
    print("BUTTON 5")
    ser.write("B5".encode('utf-8'))
def button6_pressed():
    print("BUTTON 6")
    ser.write("B6".encode('utf-8'))
def button7_pressed():
    print("BUTTON 7")
    ser.write("B7".encode('utf-8'))
def button8_pressed():
    print("BUTTON 8")
    ser.write("B8".encode('utf-8'))

"""
b1.when_pressed=button1_pressed
b2.when_pressed=button2_pressed
b3.when_pressed=button3_pressed
b4.when_pressed=button4_pressed
b5.when_pressed=button5_pressed
b6.when_pressed=button6_pressed
b7.when_pressed=button7_pressed
b8.when_pressed=button8_pressed
"""
