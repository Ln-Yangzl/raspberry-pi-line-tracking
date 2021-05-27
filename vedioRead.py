import cv2

cap = cv2.VideoCapture('testlog.avi')
ret = True
while ret:
    ret, frame = cap.read()
    cv2.imshow("display", frame)
    cv2.waitKey(0)