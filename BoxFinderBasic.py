#! /home/pi/.virtualenvs/cv/bin/python
import numpy as np
import cv2

import socket

UDP_IP = "10.35.1.2"
#UDP_IP = "10.17.48.35"
UDP_PORT = 1025
SELF_IP = "127.0.0.1"
SELF_PORT = 1026


cap = cv2.VideoCapture(0)
sizeX = 150*2
sizeY = 120*2

_NO_VALUE = 500

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while(True):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (sizeX,sizeY))

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([25,60,60])
    upper_yellow = np.array([35,255,255])

    mask = cv2.inRange(hsv,lower_yellow,upper_yellow)


    res = cv2.bitwise_and(frame,frame,mask = mask)

    blurred = cv2.GaussianBlur(mask,(7,7),0)

    ret,threshold = cv2.threshold(blurred,254,255,cv2.THRESH_BINARY)

    contours = cv2.findContours(threshold, 1, 2)

    cnt = contours[0]
    M = cv2.moments(cnt)

    x = _NO_VALUE
    y = 0
    visible = "true"
    size = 0

    if(M['m00'] == 0):
        visible = "false"
    else:
        x = int(M['m10']/M['m00'])
        x = x - sizeX / 2

        y = int(M['m01']/M['m00'])
        y = y - sizeY / 2

        size = M['m00']


    send_string = "(" + str(x) + "," + str(y) + "," + str(visible) + "," + str(size) +  ")"

    print(send_string,flush = True)
    #send values to the roborio
    #sock.sendto(str(send_string).encode('utf-8'), (UDP_IP, UDP_PORT))


    #send the values to the LED code
    #sock.sendto(str(x).encode('utf-8'), (SELF_IP, SELF_PORT))

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

