import serial
import time

ser = serial.Serial('COM5',115200,timeout=1)

print("Start")
print(ser.name)

for i in range(1):
    time.sleep(.5)

    ser.write(b'\x0501RSS0106%DW5004\x04')
    print("AUTOMATIC_PRGNO: ", ser.readline())

    ser.write(b'\x0501RSB06%DW2090\x04')
    print("AUTOMATIC_PRGNAME: ", ser.readline())

ser.close()