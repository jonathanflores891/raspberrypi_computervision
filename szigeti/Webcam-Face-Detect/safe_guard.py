#!/usr/bin/env python

import cv2
import sys
import logging as log
import datetime as dt
from datetime import datetime
from time import sleep

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)

# VideoCapture(0) if embedded laptop camera, 1 if usb camera
video_capture = cv2.VideoCapture(1)
video_capture.set(3,720)
video_capture.set(4,480)
anterior = 0

# Red rectangle
class SafeGuard():

    def __init__(self, init_point, end_point):
        self.init_point = init_point
        self.end_point  = end_point
        self.rect_color = (0,0,255)

red_rectangle = SafeGuard((100,100), (540, 400))
"""
start_point = (100, 100)
end_point = (540, 400)
"""
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    cv2.putText(frame, "Machine Status: ", (10, 20), font, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, str(datetime.now()), (10,50), font, 0.5, (0, 0, 255), 2)
    #redRectangle()
    cv2.rectangle(frame, red_rectangle.init_point, red_rectangle.end_point,
                    red_rectangle.rect_color, 1)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "X coord: {}".format(str(x)),(x,y), font, 0.8, (0, 255, 0),2)
        cv2.putText(frame, "Y coord: {}".format(str(y)),(x, y+30), font, 0.8, (0, 255, 0),2)
        print('x coord: ', x, 'y coord: ', y)
        # Change color of rectangle if face is detected

    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Safe Guard', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
