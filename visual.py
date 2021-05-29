import cv2

class visual:

    def __init__(self, camera_num = 0, verticalHeight = 180, verticalWidth = 64, horizontalHeight = 48, horizontalWidth = 320, offset = 0):
        self.offset = offset
        self.verticalHeight = verticalHeight
        self.verticalWidth = verticalWidth
        self.horizontalHeight = horizontalHeight
        self.horizontalWidth = horizontalWidth
        self.cap = cv2.VideoCapture(camera_num)

    def getOriginalPic(self):
        ret, frame = self.cap.read()
        # print(frame.shape)
        # frame = cv2.imread('test4.png')
        return frame

    def getGrayPic(self):
        frame = self.getOriginalPic()
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) 
        frame = cv2.GaussianBlur(frame,(3,3),0)
        # frame = cv2.equalizeHist(frame)
        ret,frame=cv2.threshold(frame,110,255,cv2.THRESH_BINARY_INV)
        # reticleFrame = self.__showReticle(frame)
        return frame

    def __showReticle(self, frame):
        picHeight = len(frame)
        picWidth = len(frame[0])
        # print(picHeight, picWidth)
        vertical_X = picWidth//2 - self.verticalWidth//2
        vertical_Y = picHeight//2 + self.offset
        horizontal_X = picWidth//2 - self.horizontalWidth//2
        horizontal_Y = picHeight//2 + self.offset
        frame = self.__reticle(frame, vertical_X, vertical_Y, self.verticalWidth, self.verticalHeight)
        frame = self.__reticle(frame, horizontal_X, horizontal_Y, self.horizontalWidth, self.horizontalHeight)
        return frame
    
    def __reticle(self, frame, x, y, lenX, lenY):
        # print(frame)
        # print(type(frame))
        for i in range(lenX):
            # print(y,x,i)
            frame[y][x+i] = 100
            frame[y-lenY] = 100
        for i in range(lenY):
            # print(y,x,i)
            frame[y-i][x] = 100
            frame[y-i][x+lenX] = 100
        return frame

