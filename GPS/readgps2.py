import serial
import time
import string
import pynmea2
import numpy
import math
import smbus
from time import sleep  

X_axis_H    = 0x01
Z_axis_H    = 0x05              
Y_axis_H    = 0x03             
declination = 0.08      
pi          = 3.14159265359

bus = smbus.SMBus(1)
Device_Address = 0x0d   

def Magnetometer_Init():
    bus.write_byte_data(Device_Address, 0x0a, 0x81)
    bus.write_byte_data(Device_Address, 0x0b, 0x01)
    bus.write_byte_data(Device_Address, 0x09, 0x11)  #8G
    #bus.write_byte_data(Device_Address, 0x09, 0x01)  #2G

def read_raw_data(addr):
    #Read raw 16-bit value
    low = bus.read_byte_data(Device_Address, addr-1)
    high = bus.read_byte_data(Device_Address, addr)

    #concatenate higher and lower value
    value = ((high << 8) | low)

    #to get signed value from module
    if value >= 0x8000:
        value = value - 0x10000
        return value
    else:
        return value

def get_data():
    i=0
    heading = None
    [x,y,z] = [None,None,None]
    while i<20:
        status = bus.read_byte_data(Device_Address, 0x06)
        if status == 0x04:
            x = read_raw_data(X_axis_H)
            y = read_raw_data(Y_axis_H)
            z = read_raw_data(Z_axis_H)
            continue
        if status == 0x01:
            x = read_raw_data(X_axis_H)
            y = read_raw_data(Y_axis_H)
            z = read_raw_data(Z_axis_H)
            break
        else:
            sleep(0.01)
            i+=1

    if x is None or y is None:
        [x1, y1] = [x, y]
    else:
        c=[[1.0, 0.0, 0.0],
           [0.0, 1.0, 0.0],
           [0.0, 0.0, 1.0]]
        x1 = x * c[0][0] + y * c[0][1] + c[0][2]
        y1 = x * c[1][0] + y * c[1][1] + c[1][2]
    return [x1, y1, z]
     
def get_bearing(lat1, long1, lat2, long2):
	print(type(lat1), long1, type(lat2), long2)
	dLon = (long2 - long1)
	
	x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
	y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
	brng = numpy.arctan2(x,y)
	brng = numpy.degrees(brng)
	return brng
def get_compass_result():
	[x1, y1, z] = get_data()
	if x1 is None or y1 is None:
	    heading = 0
	else:
	    heading=math.degrees(math.atan2(y1,x1))
	if(heading < 0):
	    heading = heading + 360.0 + math.degrees(declination)
	elif(heading > 360.0):
	    heading = heading - 360.0
	return heading
def calculate_bearing(hedefbearing,anlıkbearing):
	if(hedefbearing < anlıkbearing):
		return "sağa dön"
	else:
		return "sola dön"
#38.476033, 27.219424
cnmpdata=0
while True:
	chipid = bus.read_byte_data(Device_Address, 0x0d)
	Magnetometer_Init()   
	[x1, y1, z] = get_data()
	if x1 is None or y1 is None:
		heading = 0
	else:
		heading=math.degrees(math.atan2(y1,x1))
	if(heading < 0):
		heading = heading + 360.0 + math.degrees(declination)
	elif(heading > 360.0):
		heading = heading - 360.0
	cnmpdata=heading
	print("COMPAS VERİSİ " + str (cnmpdata))
	while True:
		port="/dev/ttyAMA0"
		ser=serial.Serial(port, baudrate=9600, timeout=3)
		dataout = pynmea2.NMEAStreamReader()
		newdata=str(ser.readline())
		if newdata[2:7] == "GPGGA":
			eklenecek = "0000"        
			newdata=newdata[2:-5]
			newdata = newdata[:-3] + eklenecek + newdata[-3:]
			org = "$GPGGA,100506.00,3828.54822,N,02713.19127,E,1,05,2.32,135.4,M,34.7,M,,0000*58"
			newmsg=pynmea2.parse(newdata)
			lat=newmsg.latitude
			lng=newmsg.longitude
			gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
			gpsbearing = (get_bearing(lat,lng,38.476033,27.219424))
			if(gpsbearing < 0):
				gpsbearing+=360
			print("Anlık konum bilgisi : "+gps)
			print("İstenen koordinat ile aradaki heading değeri : "+ str(gpsbearing))
			print("İstenen konum için yapılması gereken hareket "+str(calculate_bearing(gpsbearing,cnmpdata)))
			break