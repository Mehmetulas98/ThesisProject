from asyncio.windows_events import NULL
import socket
import threading
import time
# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servoPIN, GPIO.OUT)

HOST = '192.168.1.105'  # The server's hostname or IP address
PORT = 65431        # The port used by the server
XservoPIN = 2


def process_data_from_server(x):
     
    return x 
def parse_control(input):
    return input

def my_client():
        #threading.Timer(11, my_client).start()
    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            my = input("Enter command ")

            #my = "Data"

            my_inp = my.encode('utf-8')

            s.sendall(my_inp)

            while(True):
                 
                data = s.recv(1024).decode('utf-8')

                x = process_data_from_server(data)

                print("Alınan Veri : {}".format(x))

                if(x=="SON"):
                    kontrol =False
                    break
                
if __name__ == "__main__":
    while 1:
        my_client()