
"""
References:
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html
"""

import numpy as np
import cv2
import sys
from datetime import datetime

#read video file
cap = cv2.VideoCapture(1)

#check opencv version
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
#fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()  #shadow
fgbg = cv2.createBackgroundSubtractorMOG2()

font = cv2.FONT_HERSHEY_SIMPLEX

def screen_status(status, color_screen):
    cv2.putText(frame, "Machine Status: " + (status), (10, 20), font, 0.5, (color_screen), 1)

def red_rectangle(color):
    cv2.rectangle(frame, (100,100), (540, 400),
                    color, 1)

while (1):

	#if ret is true than no error with cap.isOpened
	ret, frame = cap.read()

	if ret==True:

		#apply background substraction
		fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        (im2, contours, hierarchy) = cv2.findContours(fgmask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        screen_status("ON", (0,255,0))

        cv2.putText(frame, str(datetime.now()), (10,50), font, 0.5, (0, 0, 255), 1)
        red_rectangle((0,255, 0))

        for c in contours:

            if cv2.contourArea(c) < 500:
                continue

            (x, y, w, h) = cv2.boundingRect(c)
            #draw bounding box

            cv2.putText(frame, "X : {}".format(str(x)),(x,y-40), font, 0.5, (0, 255, 0),1)
            cv2.putText(frame, "Y : {}".format(str(y)),(x,y-15), font, 0.5, (0, 255, 0),1)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if (x,y) >= (100, 100) and (x, y) <= (540, 400) or (x+w, y+h) >= (100, 100) and (x+w, y+h) <= (540, 400):
                red_rectangle((0, 0, 255))
                screen_status("OFF",(0, 0, 255))
                cv2.putText(frame, " SYSTEM ALERT ", (200,250), font, 1, (0, 0, 255), 1)

        cv2.imshow('foreground and background',fgmask)
        cv2.imshow('rgb',frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
			break


cap.release()
cv2.destroyAllWindows()
