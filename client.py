import socket
import threading
import time
import RPi.GPIO as GPIO
 
HOST = '192.168.1.105'   
PORT = 65432        

XSERVOPIN = 17
#YSERVOPIN =

GPIO.setmode(GPIO.BCM)
GPIO.setup(XSERVOPIN, GPIO.OUT)
#GPIO.setup(YSERVOPIN, GPIO.OUT)

p = GPIO.PWM(XSERVOPIN, 50)   
#p = GPIO.PWM(YSERVOPIN, 50)  
XINITPOS = 7.5
#YINITPOS = 7.5
XINITPOS=7.5
p.start(XINITPOS)  

def process_data_from_server(x):   
    return x 
def my_client():
        global XINITPOS
        #threading.Timer(11, my_client).start()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            my = input("Enter command ")
            my_inp = my.encode('utf-8')
            s.sendall(my_inp)
            if(my_inp=="Start"):
                while(True):          
                    data = s.recv(1024).decode('utf-8')
                    x = process_data_from_server(data)
                    print("Alınan Veri {}".format(x))
                    if(x.isnumeric()):
                        print(XINITPOS)
                        if(int(x) > 90):
                            if(XINITPOS+1 < 12):
                                XINITPOS+=0.5
                            p.ChangeDutyCycle(XINITPOS)
                                          
                        elif(int(x)<90):
                            if(XINITPOS-1 > 2):
                                XINITPOS-=0.5
                            p.ChangeDutyCycle(XINITPOS)
                        else:
                            pass
            else:
                # Burası 
                             
if __name__ == "__main__":
    while 1:
        my_client()
    GPIO.cleanup()