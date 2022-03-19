from turtle import delay
import serial
import time

ser = serial.Serial('COM5', baudrate=9600, timeout=0.01)  
while(1):
    
    ser.write("B4 C0 A8 01 01 00 1E\r\n".encode())
    # print("test")
    data = ser.readline()
    print(data)
    time.sleep(.1)