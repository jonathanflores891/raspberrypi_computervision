
Webcam-Face-Detect
==================

Run the program like this:

*python webcam.py*

alpython.com/blog/python/face-detection-in-python-using-a-webcam/


Update: Now supports OpenCV3. This change has been made by furetosan ( https://github.com/furetosan) and tested on Linux.

To run the OpenCV3 version, run python webcam_cv3.py haarcascade_frontalface_default.xml

////////////////////////////////////////////

import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
import RPi.GPIO as GPIO


cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)
video_capture.set(3, 320)
video_capture.set(4, 180)
anterior = 0

font = cv2.FONT_HERSHEY_SIMPLEX


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
servoPIN = 17
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) #GPIO 17 for PWM with 50Hz
p.start(0) # initialization


while True:

    #Servo angle generator
    def setAngle(angle):
        duty = angle / 18 + 2
        GPIO.output(servoPIN, True)
        p.ChangeDutyCycle(duty)
        sleep(0.2)
        GPIO.output(servoPIN, False)


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

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, 'Xpos:  Ypos:  ', (x, y), font, 0.8, (0, 255, 0), 2)
        angleValue = abs((x / 2) - 160)
        setAngle(angleValue)
        print('Coord X: ', x, 'Coord Y: ', y, 'ValueAngle: ', angleValue)
        '''
    #Servo testing
        if x > 100:
            setAngle()
            print('x greater than 100')
        elif y < 95:
            setAngle(0)
            print('y minor than 200')
        '''

    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))


    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
