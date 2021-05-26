import cv2
from controler import speedControler

class houghTracking():

    def __init__(self, rho, theta, threshold, minLineLength, maxLineGap, lineBoundary, lossBoundary, slopScale, offsetScale):
        self.houghagrs = (rho, theta, threshold, minLineLength, maxLineGap)
        self.lineBoundary = lineBoundary
        self.lossBoundary = lossBoundary
        self.slopScale = slopScale
        self.offsetScale = offsetScale
        self.speedThread = speedControler()
        self.speedThread.start()

    def computeLoss(self, frame, end = '\n'):
        lines = cv2.HoughLinesP(frame,*self.houghagrs)
        loss, line, offset = self.__findLine(lines)
        if abs(loss + offset) < self.lossBoundary:
            loss = -self.speedThread.speedLoss()
            print('speedLoss:', loss, end=' ')
        else:
            print('slop:%f, offset:%f'%(loss, offset), end=' ')
        print('lspeed:%f rspeed:%f'%(self.speedThread.getSpeed()), end=end)
        return loss + offset, line
    
    # 寻找斜率最小且在指定boundary内的直线
    def __findLine(self, lines):
        if type(lines) == type(None):
            lines = [[[0,0,0,0]]]
        slop = 1<<31
        sign = True
        line = ((320,260),(320,260))
        for item in lines:
            # print('item:',item)
            for x1,y1,x2,y2 in item:
                currentSlop = 1<<31
                if y2 < self.lineBoundary:
                    currentSlop = self.__computeSlop(x1,y1,x2,y2)
                    currentSign = currentSlop > 0
                if abs(currentSlop) < slop:
                    slop = abs(currentSlop)
                    sign = currentSign
                    line = ((x1,y1),(x2,y2))
        slop = min(slop, 1)*(sign*2-1) * self.slopScale
        offset = (320 - line[1][0]) * self.offsetScale
        return slop, line, offset

    def __computeSlop(self, x1, y1, x2, y2):
        if y1 == y2:
            return 1<<31
        return (x2-x1)/(y2-y1)

    def __del__(self):
        self.speedThread.stop()
