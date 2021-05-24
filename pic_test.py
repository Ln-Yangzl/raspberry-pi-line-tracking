import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) 
frame = cv2.equalizeHist(frame)
ret,frame=cv2.threshold(frame,80,255,cv2.THRESH_BINARY_INV)
print(len(frame))
print(len(frame[0]))
print(frame)
cv2.imshow("display", frame)  # 显示
cv2.waitKey(0)