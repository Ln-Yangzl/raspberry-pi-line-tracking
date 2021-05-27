from controler import speedControler
import cv2

class edgeTracking:

    def __init__(self, firstLineY, secondLineY, lossBoundary, slopScale, slopBound):
        self.firsetLineY = firstLineY
        self.secondLineY = secondLineY
        self.lossBoundary = lossBoundary
        self.slopScale = slopScale
        self.slopBound = slopBound
        self.speedThread = speedControler()
        self.speedThread.start()

    def computeLoss(self, frame, end = '\n'):
        height, width = frame.shape[:2]
        mid = width // 2
        # height = len(frame)
        # mid = len(frame[0]) // 2
        frame = cv2.GaussianBlur(frame,(3,3),0)
        frame = cv2.Canny(frame, 50, 150, apertureSize=3)
        x1, y1, x2, y2 = self.__getEdgePos(frame)
        slop1 = self.__computeSlop(mid, height, x1, y1)
        slop2 = self.__computeSlop(mid, height, x2, y2)
        slop = 0
        if abs(slop1) < abs(slop2):
            slop = slop1
        else:
            slop = slop2
            x1, y1, x2, y2 = x2, y2, x1, y1
        # 限制斜率最大绝对值为1，避免正切值在角度过大时值过大
        slop = min(abs(slop), self.lossBoundary) * ((slop>0)*2-1)
        loss = slop * self.slopScale
        if abs(loss) < self.lossBoundary:
            loss = self.speedThread.speedLoss()
            print('speedLoss', loss, end=' ')
        else:
            print('slopLoss:', loss, end=' ')
        print('lspeed:%f rspeed:%f'%(self.speedThread.getSpeed()), end=end)
        cv2.circle(frame, (x1, y1), 10, (100, 0, 0), 1)
        cv2.circle(frame, (x2, y2), 10, (100, 0, 0), 1)
        cv2.line(frame, (height, mid), (x1, y1), (0,100,0), 1)
        return loss, frame


        
    def __computeSlop(x1, y1, x2, y2):
        if y1 == y2 or x1 == -1 or x2 == -1:
            return 1<<31
        return (x2-x1)/(y2-y1)

    # 如果未找到返回坐标（-1，-1）
    def __getEdgePos(self, edges):
        x1, y1 = self.__findEdgeMid(edges[self.firsetLineY]), self.firsetLineY
        x2, y2 = self.__findEdgeMid(edges[self.secondLineY]), self.secondLineY
        return x1, y1, x2, y2
        

    def __findEdgeMid(self, edge):
        width = len(edge)
        mid = width // 2
        pos = -1
        leftEdge = -1
        for i in range(width):
            if edge[i] != 0:
                if leftEdge == -1:
                    leftEdge == i
                else:
                    currentPos = (leftEdge + i) // 2
                    if abs(currentPos - mid) < abs(pos - mid):
                        pos = currentPos
                    leftEdge = -1
        return pos


    def __del__(self):
        self.speedThread.stop()