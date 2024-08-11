import serial
import time

ser = serial.Serial('COM5',115200,timeout=1)

print("Start")
print(ser.name)


# PRG.NO / D131
# BOND_NAME / D132 / 8W
# LOT_NO / D140 / 5W
# RPM / D120
# TIME_SET / D122
# TIME_ACT / D220

#ser.write(b'\x0501WSS0106%PW002FFFF\x04') #Light on
# ser.write(b'\x0501RSS0106%DW131\x04')
# print(ser.readline())

for i in range(1):
    time.sleep(.5)

    ser.write(b'\x0501RSS0106%DW131\x04')
    print("PRG.NO: ", ser.readline())

    ser.write(b'\x0501RSB06%DW13208\x04')
    print("BOND_NAME: ", ser.readline())

    ser.write(b'\x0501RSB06%DW14005\x04')
    print("LOT_NO: ", ser.readline())

    ser.write(b'\x0501RSS0106%DW120\x04')
    print("RPM: ", ser.readline())

    ser.write(b'\x0501RSS0106%DW122\x04')
    print("TIME_SET: ", ser.readline())

    ser.write(b'\x0501RSS0106%DW220\x04')
    print("TIME_ACT: ", ser.readline())

ser.close()

# \x05 - 01 - W - SS - 01 - 06 - %PW002 - FFFF - \x04

# 헤더 : ENQ (\x05)
# 국번 : 01
# 명령어 : W
# 명령어 타입 : SS
# 블록수 : 01
# 변수의 길이 : 06
# 변수 이름 : %PW002
# 데이터 (16진수) : FFFF
# 테일 : EOT (\x04)


# \x0501RSS0106%DW122\x04

# 헤더 : ENQ (\x05)
# 국번 : 01
# 명령어 : R
# 명령어 타입 : SS
# 블록수 : 01
# 변수의 길이 : 06
# 변수 이름 : %DW122
# 테일 : EOT (\x04)


# 데이터 쓰기 ACK응답 형식

# 헤더 : ACK
# 국번 : 01
# 명령어 : R
# 명령어 타입 : SS
# 테일 : EOT (\x04)


# 데이터 읽기 ack응답 형식

# 헤더 : ACK (\x06)
# 국번 : 01
# 명령어 : R
# 명령어 타입 : SS
# 블록수 : 01
# 데이터갯수 : 02 <- 32BIT씩 나눈 데이터 길이(02 -> 총 64BIT)
# 데이터
# 테일 : ETX

# 결과 16진수 아스키로 반환

# b'\x0601RSS0102000A\x03'
# b'\x06-01-R-SS-01-02-000A-\x03'



4241 - 4443 - 4645 - 3231 - 3433 - 000000000000
abcde1234


44 41-32 43-00 35- 00000000

d a - 2 c - 0 5 
3 a - 0 4

