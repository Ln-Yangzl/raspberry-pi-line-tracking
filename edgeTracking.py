import cv2

class edgeTracking:

    def __init__(self, firstLineY, secondLineY, slopBound1, slopBound2, slopScale1, slopScale2):
        self.firsetLineY = firstLineY
        self.secondLineY = secondLineY
        self.slopBound1 = slopBound1
        self.slopBound2 = slopBound2
        self.preSlop = 0
        self.slopScale1 = slopScale1
        self.slopScale2 = slopScale2


    def computeLoss(self, frame, end = '\n'):
        height, width = frame.shape[:2]
        mid = width // 2
        # height = len(frame)
        # mid = len(frame[0]) // 2
        # frame = cv2.GaussianBlur(frame,(3,3),0)
        frame = cv2.Canny(frame, 50, 120, apertureSize=3)
        x1, y1, x2, y2 = self.__getEdgePos(frame)
        # print('get position:', x1, y1, x2, y2)
        slop1 = self.__computeSlop(mid, height, x1, y1)
        slop2 = self.__computeSlop(mid, height, x2, y2)
        slop = 0
        if abs(slop1) < abs(slop2):
            slop = slop1
        else:
            slop = slop2
            x1, y1, x2, y2 = x2, y2, x1, y1
        # 如果丢失视野，则使用上一次的斜率
        if abs(slop) == 1<<31:
            slop = self.preSlop
        self.preSlop = slop
        # 限制斜率正切值，避免过大
        print('slop:%.4f'%slop, end=' ')
        absSlop = abs(slop)
        loss = 0
        if absSlop < self.slopBound1:
            loss = slop * self.slopScale1
        elif absSlop >= self.slopBound1 and absSlop < self.slopBound2:
            loss = self.slopBound1 * ((slop>0)*2-1)
        else:
            loss = slop * self.slopScale2
        # loss = min(abs(slop), self.slopBound) * ((slop>0)*2-1)
        print('slopLoss:%.4f'%loss, end=end)
        print('\t', end='')
        # 在图中画出标识标线
        if x1 != -1:
            cv2.circle(frame, (x1, y1), 10, (100, 0, 0), 1)
        if x2 != -1:
            cv2.circle(frame, (x2, y2), 10, (100, 0, 0), 1)
        # print('target line: ', mid, height, x1, y1)
        cv2.line(frame, (mid, height), (x1, y1), (100,0,0), 1)
        cv2.line(frame, (0, self.firsetLineY), (width, self.firsetLineY), (100,0,0), 1)
        cv2.line(frame, (0, self.secondLineY), (width, self.secondLineY), (100,0,0), 1)
        return loss, frame


    def __computeSlop(self, x1, y1, x2, y2):
        if y1 == y2 or x1 == -1 or x2 == -1:
            return 1<<31
        return (x1-x2)/(y2-y1)

    # 如果未找到返回的x坐标为-1
    def __getEdgePos(self, edges):
        x1, y1 = self.__findEdgeMid(edges[self.firsetLineY]), self.firsetLineY
        x2, y2 = self.__findEdgeMid(edges[self.secondLineY]), self.secondLineY
        return x1, y1, x2, y2
        
    # 寻找两条道路边缘线的中点
    def __findEdgeMid(self, edge):
        width = len(edge)
        mid = width // 2
        pos = -1
        leftEdge = -1
        for i in range(width):
            if edge[i] != 0:
                if leftEdge == -1:
                    leftEdge = i
                else:
                    currentPos = (leftEdge + i) // 2
                    if abs(currentPos - mid) < abs(pos - mid):
                        pos = currentPos
                    leftEdge = -1
        # 只有一根线被识别，使用该线
        if pos == -1:
            pos = leftEdge
        return pos


