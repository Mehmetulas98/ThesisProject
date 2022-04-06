import serial
import time
import string
import pynmea2
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
		print(gps)