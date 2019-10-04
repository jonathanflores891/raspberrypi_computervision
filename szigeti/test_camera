import cv2

cap = cv2.VideoCapture(0)

if (cap.isOpened() == False):
	print("Error opening video stream or file")
	
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,480)

while(True):
	ret, frame = cap.read()
	if ret == True:
		cv2.imshow('frame', frame)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			break
cap.release()

cv2.destroyAllWindows()

