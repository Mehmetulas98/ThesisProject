
from json.tool import main
from PIL import Image
import time
import socket
from turtle import position
import numpy as np
from traceback import print_tb
from PIL import ImageGrab
import cv2
from numpy import array
from keyboardInput import *
import sys


###
net = cv2.dnn.readNet("../weights/yolov3.weights", "../cfg/yolov3.cfg")
classes = []
with open("../coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = net.getUnconnectedOutLayersNames()
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading image
cap = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0
mon = {'top': 160, 'left': 160, 'width': 500, 'height': 500}

x_medium = 218
x_servo_position = 90
x_center = 218
###


def detect(Screen, frame_id=frame_id):
    global x_servo_position
    height, width, channels = Screen.shape
    frame_id += 1
    # Detecting objects
    blob = cv2.dnn.blobFromImage(
        Screen, 1/255, (416, 416), (0, 0, 0), True, crop=False)
    # print(blob.shape)
    net.setInput(blob)
    # Showing informations on the screen
    outs = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if(class_id == 0):

                if confidence > 0.2:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.3)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]

            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = colors[class_ids[i]]
            cv2.rectangle(Screen, (x, y),
                          (x + w, y + h), color, 2)
            start_point = (0, 0)
            x_medium = int((x+x+w)/2)
            y_medium = int((y+y+h)/2)
            end_point = (250, 250)
            cv2.line(Screen, (x_medium, 0),
                     (x_medium, 480), (255, 14, 0), 3)
            cv2.line(Screen, (480, y_medium),
                     (0, y_medium), (255, 14, 0), 3)

            if(x_medium < x_center-30):
                x_servo_position = 95
            elif(x_medium > x_center+30):
                x_servo_position = 85
            else:
                x_servo_position = 90

            cv2.putText(
                Screen, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, color, 3)
    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    cv2.putText(Screen, "FPS: " + str(round(fps, 2)),
                (10, 50), font, 4, (0, 0, 0), 3)

    cv2.imshow("Image", Screen)

    return(x_servo_position)


HOST = '192.168.1.104'
PORT = 65433
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
global a
print("kotnrol")
clientsocket, address = s.accept()
print(f"Connection from {address} has been established.")
#clientsocket.send(bytes("Hey there : ", "utf-8"))
with clientsocket:
    data = clientsocket.recv(1024).decode('utf-8')
    if(str(data) == "Start"):
        print("!!! Servo Motora Konum Bilgisi Gönderilmeye Başlanıyor !!!")
        time.sleep(3)
        #
        cap = cv2.VideoCapture(1)
        #
        while True:

            ##
            _, frame = cap.read()
            Screen = array(frame)

            ##
            #Screen = array(ImageGrab.grab(bbox=(400, 400, 800, 800)))
            a = detect(Screen)
            print(a)
            key = cv2.waitKey(1)
            if key == 27:
                break
            #timee = str(time.time())
            timee = str(a)
            try:
                clientsocket.send(bytes(timee, "utf-8"))
                print("Veri gönderildi")
            except:
                pass

    if(str(data) == "Manuel"):
        print("!!! Servo Motora Hareket Bilgisi Gönderilmeye Başlanıyor !!!")
        time.sleep(3)
        while True:
            result = keyboardinput()
            print(result)
            try:
                clientsocket.send(bytes(result, "utf-8"))
            except:
                print("İşlem Durduruldu !!!")
                clientsocket.send(bytes("SON", "utf-8"))
                break
            if(result == None):
                clientsocket.send(bytes("SON", "utf-8"))
                break
