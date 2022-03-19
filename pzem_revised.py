# Reading PZEM-004t power sensor (new version v3.0) through Modbus-RTU protocol over TTL UART
# Run as:
# python3 pzem_004t.py

# To install dependencies: 
# pip install modbus-tk
# pip install pyserial

import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import numpy as np

from flask import Flask, request, abort



#======python的函數庫==========
import tempfile, os
import datetime
import time
import traceback
#======python的函數庫==========

#======google試算表======
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)

client = gspread.authorize(creds)
sheet = client.open("Energy_Chart")
sheet_device = sheet.get_worksheet(0)
#======google試算表======

DEBUG_MODE = 1
COM_PORT = 'COM6'

if (not DEBUG_MODE):
    # Connect to the sensor
    sensor = serial.Serial(
                        port=COM_PORT,
                        baudrate=9600,
                        bytesize=8,
                        parity='N',
                        stopbits=1,
                        xonxoff=0
                        )

    master = modbus_rtu.RtuMaster(sensor)
    master.set_timeout(2.0)
    master.set_verbose(True)

n = int(sheet_device.cell(1,2).value)
i=0

while(True):
    try:
        if (not DEBUG_MODE):
            data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

            voltage = data[0] / 10.0 # [V]
            current = (data[1] + (data[2] << 16)) / 1000.0 # [A]
            power = (data[3] + (data[4] << 16)) / 10.0 # [W]
            energy = data[5] + (data[6] << 16) # [Wh]
            frequency = data[7] / 10.0 # [Hz]
            powerFactor = data[8] / 100.0
            alarm = data[9] # 0 = no alarm
        else:
            voltage,current = 110+np.random.normal(0,1),0.023+np.random.normal(0,0.01)
            power, energy, frequency, powerFactor, alarm = voltage*current, 1, 60, .7,1

        print('Voltage [V]: ', voltage)
        print('Current [A]: ', current)
        print('Power [W]: ', power) # active power (V * I * power factor)
        print('Energy [Wh]: ', energy)
        print('Frequency [Hz]: ', frequency)
        print('Power factor []: ', powerFactor)
        print('Alarm : ', alarm)
        n = n + 1
        sheet_device.update_cell(n, 1, str(voltage*current))
        sheet_device.update_cell(1, 2, str(n))
        i+=1

    except KeyboardInterrupt:
        break
    except:
        print("data not available")

# Changing power alarm value to 100 W
# master.execute(1, cst.WRITE_SINGLE_REGISTER, 1, output_value=100)

if(not DEBUG_MODE):
    try:
        master.close()
        if sensor.is_open:
            sensor.close()
    except:
        pass