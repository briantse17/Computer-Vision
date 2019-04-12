import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:

    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_orange = np.array([0,160, 0])
    upper_orange = np.array([200,255,255])

    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    result = cv2.bitwise_and(frame, frame, mask = mask)

    #kernel = np.ones((15,15), np.float32)/225
    #smoothed = cv2.filter2D(result, -1, kernel)
    #median = cv2.medianBlur(result, 15)

    blur = cv2.GaussianBlur(result, (15,15), 0)


    cv2.imshow("frame", frame)
    cv2.imshow("result", result)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
       False
cv2.destroyAllWindows()
cap.release()

