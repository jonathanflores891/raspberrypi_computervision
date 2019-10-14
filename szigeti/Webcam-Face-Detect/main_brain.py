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

in1 = 24
in2 = 23
en = 25
temp1=1

in3 = 20
in4 = 16
en1 = 26

GPIO.setmode(GPIO.BCM)
servoPIN = 17
GPIO.setup(servoPIN, GPIO.OUT)

# Motor Control I/O

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(en,1000)
p1=GPIO.PWM(en1,1000)
p.start(30)
p1.start(30)

p2 = GPIO.PWM(servoPIN, 50) #GPIO 17 for PWM with 50Hz
p2.start(90) # initialization


while True:

    #x = raw_input()

    #Servo angle generator
    def setAngle(angle):
        duty = angle / 18 + 2
        GPIO.output(servoPIN, True)
        p2.ChangeDutyCycle(duty)
        sleep(0.2)
        GPIO.output(servoPIN, False)

#Motor Drivers

    def stop():
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        p.ChangeDutyCycle(30)
        p1.ChangeDutyCycle(30)
        print("Stop")

    def forward():
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        p.ChangeDutyCycle(40)
        p1.ChangeDutyCycle(40)
        print("Forward")

    def backward():
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        p.ChangeDutyCycle(30)
        p1.ChangeDutyCycle(30)
        print("Backward")

    def left():
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        p.ChangeDutyCycle(30)
        p1.ChangeDutyCycle(30)
        print("Left")

    def right():
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        p.ChangeDutyCycle(30)
        p1.ChangeDutyCycle(30)
        print("Right")


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
        if x <130:
           left()

        if x > 200:
            right()

        if x > 130 and x < 200:
            forward()


    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
        stop()

    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
GPIO.cleanup()
