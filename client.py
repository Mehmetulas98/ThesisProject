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
            elif(my_inp == "Manuel"):
                # Burada gelen kodlara göre araba hareket ettirilecek 
                pass
            elif(my_inp == "Otonom"):
                #
                #START_GPS_POSITION = []
                #FINISH_GPS_POSITION = []
                #CURRENT_GPS_POSITION = []
                # CURRENT_ANGLE = get_angle()
                while(True):
                    # Hedef ile anlık koordinat arasındaki açı farkını bul
                    # angle=get_bearing(CURRENT_GPS_POSITION[0],CURRENT_GPS_POSITION[1],FINISH_GPS_POSITION[0],FINISH_GPS_POSITION[1])
                    
                    # # 2 sn düz git

                    # # yön düzelt
                    # if(abs(angle - CURRCURRENT_ANGLE) > 180):
                    #     while(angle != CURRENT_ANGLE):
                    #         #sağa dön
                    #         pass
                    #     break
                    # else:
                    #     while(angle != CURRENT_ANGLE):
                    #         #sola dön
                    #         pass
                    #     break

                    # # GPS pozisyon bilgisi al
                    # CURRRNT_GPS_POSITION = get_GPS_position()
                    # if(get_distances(CURRENT_GPS_POSITION[0],CURRENT_GPS_POSITION[1],FINISH_GPS_POSITION[0],FINISH_GPS_POSITION[1]) <= 6):
                    #     # İstenen bölgeye girildi
                    #     print("! İstenen Konuma Varıldı !")
                    #     break
                             
if __name__ == "__main__":
    while 1:
        my_client()
    GPIO.cleanup()