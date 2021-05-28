import cv2

cap = cv2.VideoCapture('testlog.avi')
ret = True
while ret:
    ret, frame = cap.read()
    cv2.imshow("display", frame)
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        cv2.destroyAllWindows()
        break