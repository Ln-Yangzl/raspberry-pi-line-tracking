from controler import speedControler

class tracking:

    def __init__(self, verticalHeight = 20, verticalWidth = 4, horizontalHeight = 4, horizontalWidth = 20, verticalLossBound = 0.8, lossScale = 0.005):
        self.verticalLossBound = verticalLossBound
        self.lossScale = lossScale
        self.verticalSum = 100000000000000000
        self.verticalHeight = verticalHeight
        self.verticalWidth = verticalWidth
        self.horizontalHeight = horizontalHeight
        self.horizontalWidth = horizontalWidth
        # get weights: [-3, -2, -1, 0, 1, 2, 3] if horizontalWidth = 7
        self.horizontalWeights = self.__computeHorizontalWeights(horizontalWidth)
        self.speedThread = speedControler()
        self.speedThread.start()



    def computeLoss(self, frame, end = '\n'):
        loss = 0
        vertical, horizontal =  self.__getTargetBlock(frame)
        # print('vertical:')
        # print(vertical)
        # print('horizontal:')
        # print(horizontal)
        currentVerticalSum = self.__computeVerticalSum(vertical)
        print(' verticalSum:', currentVerticalSum, end='')
        if currentVerticalSum < self.verticalSum * self.verticalLossBound:
            loss = self.__computeHorizontalLoss(horizontal)
            print(' horizontalLoss:', loss, end='')
        else:
            loss = self.speedThread.speedLoss()
            print(' speedLoss:', loss, end='')
        print('', end = end)
        return loss

    def updateVerticalSum(self, frame):
        vertical, _ = self.__getTargetBlock(frame)
        verticalSum = self.__computeVerticalSum(vertical)
        print('update vertical sum: ', verticalSum)
        self.verticalSum = verticalSum

    def __computeVerticalSum(self, vertical):
        sum = 0
        for i in range(self.verticalHeight):
            for j in range(self.verticalWidth):
                # not(not(x)) = 255 --> 1, 0 --> 0
                sum += not(not(vertical[i][j]))
        return sum

    def __computeHorizontalLoss(self, horizontal):
        res = 0
        for i in range(self.horizontalHeight):
            res += sum(map(lambda x,y:(not(not(x)))*y, horizontal[i], self.horizontalWeights))
        return res/self.lossScale


    def __getTargetBlock(self, frame):
        picHeight = len(frame)
        picWidth = len(frame[0])
        vertical_X = picWidth//2 - self.verticalWidth//2
        vertical_Y = picHeight//2
        horizontal_X = picWidth//2 - self.horizontalWidth//2
        horizontal_Y = picWidth//2
        vertical = []
        horizontal = []
        for i in range(self.verticalHeight):
            vertical.append(frame[i + vertical_Y][vertical_X : vertical_X + self.verticalWidth].tolist())
        for i in range(self.horizontalHeight):
            horizontal.append(frame[i + horizontal_Y][horizontal_X : horizontal_X + self.horizontalWidth].tolist())
        return vertical, horizontal


    def __computeHorizontalWeights(self, horizontalWidth):
        start = -(horizontalWidth//2)
        res = []
        for i in range(horizontalWidth):
            start += i
            res.append(i)
        return res

    def __del__(self):
        self.speedThread.stop()

