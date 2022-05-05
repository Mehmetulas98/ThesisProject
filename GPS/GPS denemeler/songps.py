import serial              
from time import sleep
import sys
ser = serial.Serial ('/dev/ttyAMA0')
gpgga_info = '$GPGGA,'
GPGGA_buffer = 0
NMEA_buff = 0
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - (int(decimal_value)))/0.6
    position = degrees + mm_mmmm
    position = '%.4f' %(position)
    return position
try:
    while True:
        received_data = (str)(ser.readline()) #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split('$GPGGA,',1)[1]  #store data coming after “$GPGGA,” string
            NMEA_buff = (GPGGA_buffer.split("','"))
            nmea_time = []
            nmea_latitude = []
            nmea_longitude = []
            nmea_time = NMEA_buff[0]
            data = nmea_time
            data_splitted = data.split(',')
            print(data_splitted)
            latitute = data_splitted[1]
            longitute = data_splitted[3]
            print ("NMEA Latitude:", latitute,"NMEA Longitude:", longitute,'\n')
            try:
                cornrer = convert_to_degrees(float(latitute))
                print(cornrer)
            except:
                pass
except KeyboardInterrupt:
    sys.exit(0)