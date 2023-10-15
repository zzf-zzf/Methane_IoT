#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time
import random

ser = serial.Serial('/dev/ttyS0',9600)
ser.flushInput()

powerKey = 4
rec_buff = ''

def read_file(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data

def powerOn(powerKey):
    print('SIM7070X is starting:')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(powerKey,GPIO.OUT)
    time.sleep(0.1)
    GPIO.output(powerKey,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(powerKey,GPIO.LOW)
    time.sleep(5)
    ser.flushInput()
    print('SIM7070X is ready')

def powerDown(powerKey):
    print('SIM7070X is loging off:')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(powerKey,GPIO.OUT)
    GPIO.output(powerKey,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(powerKey,GPIO.LOW)
    time.sleep(5)
    print('Good bye')
    
def sendAt(command,back,timeout):
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.1 )
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(command + ' back:\t' + rec_buff.decode())
            return 0
        else:
            print(rec_buff.decode())
            return 1
    else:
        print(command + ' no responce')

def checkStart():
    while True:
        # simcom module uart may be fool,so it is better to send much times when it starts.
        ser.write( 'AT\r\n'.encode() )
        time.sleep(1)
        ser.write( 'AT\r\n'.encode() )
        time.sleep(1)
        ser.write( 'AT\r\n'.encode() )
        time.sleep(1)
        if ser.inWaiting():
            time.sleep(0.01)
            recBuff = ser.read(ser.inWaiting())
            print('SOM7080X is ready\r\n')
            print( 'try to start\r\n' + recBuff.decode() )
            if 'OK' in recBuff.decode():
                recBuff = ''
                break 
        else:
            powerOn(powerKey)

def main():
    # filename = "/home/pi/rasp_mqtt/data.txt"
    # data = read_file(filename)
    # len_byte = len(data.encode())
    num_data = 5
    checkStart()
    print('wait for signal')
    time.sleep(4)
    sendAt('AT+CSQ','OK',1)
    sendAt('AT+CPSI?','OK',1)
    # sendAt('AT+CGREG?','+CGREG: 0,1',0.5)
    sendAt('AT+CNACT=0,1','OK',1)# not working (active)
    sendAt('AT+CACID=0', 'OK',1)
    sendAt('AT+SMCONF=\"URL\",b97b659315cf4f0cafd48b90e3421aa6.s2.eu.hivemq.cloud,8883','OK',1)
    sendAt('AT+SMCONF=\"USERNAME\",psusnec','OK',1)
    sendAt('AT+SMCONF=\"PASSWORD\",Psusnec06','OK',1)
    sendAt('AT+SMCONF=\"KEEPTIME\",60','OK',1)
    sendAt('AT+SMCONF=\"CLIENTID\",ZHOU','OK',1)

    sendAt('AT+CSSLCFG=\"SSLVERSION\",1,3','OK',1)
    sendAt('AT+CSSLCFG=\"CIPHERSUITE\",1,0,0xC02F','OK',1)
    sendAt('AT+CSSLCFG=\"SNI\",1,b97b659315cf4f0cafd48b90e3421aa6.s2.eu.hivemq.cloud','OK',1)
    sendAt('AT+CSSLCFG=\"CTXINDEX\",1','OK',1)
    sendAt('AT+SMSSL=2,\"ca.crt\",\"myclient.crt\"','OK',1)


    sendAt('AT+SMCONN','OK',5)
    time.sleep(3)

    for i in range(num_data):
        data = random.randint(0,100)
        data = str(data)
        len_byte = len(data.encode())
        sendAt('AT+SMPUB=\"methane/mqtt\",%d,1,0'%len_byte,'OK',1)
        ser.write(data.encode())
        time.sleep(3)
    #print('send message successfully!')
    sendAt('AT+SMDISC','OK',1)
    sendAt('AT+CNACT=0,0', 'OK', 1)
    powerDown(powerKey)


if __name__ == "__main__":
    main()


