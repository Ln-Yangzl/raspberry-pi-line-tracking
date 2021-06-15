import time
import RPi.GPIO as GPIO
import threading
from pid import PID


EA, I2, I1, EB, I4, I3, LS, RS = (13, 19, 26, 16, 20, 21, 6, 12)
FREQUENCY = 50

class controler:

    def __init__(self, LP, LI, LD, L_init_duty, RP, RI, RD, R_init_duty, target_duty, lossBoundary, lossScale, sleepBound, sleepTime, sleepLoss):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
        GPIO.output([EA, I2, EB, I3], GPIO.LOW)
        GPIO.output([I1, I4], GPIO.HIGH)
        self.pwma = GPIO.PWM(EA, FREQUENCY)
        self.pwmb = GPIO.PWM(EB, FREQUENCY)
        self.pwma.start(0)
        self.pwmb.start(0)
        self.L_control = PID(LP, LI, LD, L_init_duty)   # for pwma
        self.R_control = PID(RP, RI, RD, R_init_duty)   # for pwmb
        self.ideal_duty = target_duty
        self.L_pre_duty = 0
        self.R_pre_duty = 0
        self.L_init_duty = L_init_duty
        self.R_init_duty = R_init_duty
        self.lossScale = lossScale
        self.lossBoundary = lossBoundary
        self.speedThread = speedControler()
        # True: 上一次进入update为速度loss或初始状态
        # False: 上一次进入update为斜率loss状态
        # self.stage = True
        self.sleepBound = sleepBound
        self.sleepTime = sleepTime
        self.sleepLoss = sleepLoss


    def update(self, loss):
        Lnext = self.L_pre_duty
        Rnext = self.R_pre_duty
        # if abs(loss) < self.lossBoundary:
        #     if self.stage:
        #         speedLoss = -self.speedThread.speedLoss()
        #         self.R_pre_duty = self.R_control.update(speedLoss)
        #         Rnext = self.R_pre_duty
        #         # speedLoss = self.speedThread.speedLoss()
        #         # self.L_pre_duty = self.L_control.update(speedLoss)
        #         # Lnext = self.L_pre_duty
        #     self.stage = True
        # else:
        #     self.stage = False
        #     loss = -loss * self.lossScale
        #     if loss > 0:
        #         Lnext = max(Lnext - loss, 0)
        #         # Rnext = min(Lnext + loss, 100)
        #     else:
        #         Rnext = max(Rnext + loss, 0)
        #         # Lnext = min(Rnext - loss, 100)
        isSleep = False
        if abs(loss) >= self.sleepTime:
            isSleep = True
            if self.sleepLoss != 0:
                loss = self.sleepLoss * ((loss>0)*2-1)
        loss = -loss * self.lossScale
        if loss > 0:
            Lnext = max(Lnext - loss, 0)
            # Rnext = min(Lnext + loss, 100)
        else:
            Rnext = max(Rnext + loss, 0)
            # Lnext = min(Rnext - loss, 100)

        # print(' Lduty:',self.L_pre_duty,' Rduty:',self.R_pre_duty)
        print('Lduty:%.2f Rduty:%.2f'%(Lnext,Rnext), end = ' ')
        print('Lspeed:%.2f Rspeed:%.2f'%(self.speedThread.getSpeed()))
        self.pwma.ChangeDutyCycle(Lnext)
        self.pwmb.ChangeDutyCycle(Rnext)
        if isSleep:
            time.sleep(self.sleepTime)
            

    def run(self):
        self.L_pre_duty = self.L_init_duty
        self.R_pre_duty = self.R_init_duty
        self.speedThread.start()
        self.__updateDuty(self.L_pre_duty)
        time.sleep(0.1)

    def stop(self):
        self.L_pre_duty = 0
        self.R_pre_duty = 0
        self.speedThread.stop()
        self.__updateDuty(0)
        

    def __updateDuty(self, target):
        self.pwma.ChangeDutyCycle(target)
        self.pwmb.ChangeDutyCycle(target)

    def __del__(self):
        self.pwma.stop()
        self.pwmb.stop()
        GPIO.cleanup()


class speedControler(threading.Thread):

    def __init__(self):
        super().__init__()
        self.rspeed = 0
        self.lspeed = 0
        self.lcounter = 0
        self.rcounter = 0
        # control the thread end
        self.isStop = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([LS, RS],GPIO.IN)
        GPIO.add_event_detect(LS,GPIO.RISING,callback=self.__my_callback)
        GPIO.add_event_detect(RS,GPIO.RISING,callback=self.__my_callback)

    def run(self):
        self.isStop = False
        while not(self.isStop):
            self.rspeed=(self.rcounter/20.00)
            self.lspeed=(self.lcounter/20.00)
            self.rcounter = 0
            self.lcounter = 0
            time.sleep(0.1)

    def speedLoss(self):
        return self.rspeed - self.lspeed
    
    def getSpeed(self):
        return self.lspeed, self.rspeed
    
    def stop(self):
        self.isStop = True

    def __my_callback(self, channel):
        if (channel==LS):
            self.lcounter+=1
        elif(channel==RS):
            self.rcounter+=1

    def __del__(self):
        GPIO.cleanup()


# class directionControler:

#     def __init__(self, LP, LI, LD, L_init_duty, RP, RI, RD, R_init_duty, target_duty = 80):
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
#         GPIO.output([EA, I2, EB, I3], GPIO.LOW)
#         GPIO.output([I1, I4], GPIO.HIGH)
#         self.pwma = GPIO.PWM(EA, FREQUENCY)
#         self.pwmb = GPIO.PWM(EB, FREQUENCY)
#         self.pwma.start(0)
#         self.pwmb.start(0)
#         self.L_control = PID(LP, LI, LD, L_init_duty)   # for pwma
#         self.R_control = PID(RP, RI, RD, R_init_duty)   # for pwmb
#         self.ideal_duty = target_duty
#         self.L_pre_duty = L_init_duty
#         self.R_pre_duty = R_init_duty
#         self.L_init_duty = L_init_duty
#         self.R_init_duty = R_init_duty


#     def update(self, loss, isStop = False, isRun = False):
#         # print('loss:', loss, end='')
#         if self.L_pre_duty < self.ideal_duty:
#             self.L_pre_duty = self.L_control.update(loss)
#         else:
#             self.R_pre_duty = self.R_control.update(-loss)
#         # if loss > 0:
#         #     if self.L_pre_duty < self.ideal_duty:
#         #         self.L_pre_duty = self.L_control.update(-loss)
#         #     else:
#         #         self.R_pre_duty = self.R_control.update(loss)
#         # elif loss < 0:
#         #     if self.L_pre_duty > self.ideal_duty:
#         #         self.L_pre_duty = self.L_control.update(-loss)
#         #     else:
#         #         self.R_pre_duty = self.R_control.update(loss)
#         if isStop:
#             self.L_pre_duty = 0
#             self.R_pre_duty = 0
#         if isRun:
#             self.L_init_duty = self.L_init_duty
#             self.R_init_duty = self.R_init_duty

#         # print(' Lduty:',self.L_pre_duty,' Rduty:',self.R_pre_duty)
#         print('Lduty:%.2f Rduty:%.2f'%(self.L_pre_duty,self.R_pre_duty))
#         self.pwma.ChangeDutyCycle(self.L_pre_duty)
#         self.pwmb.ChangeDutyCycle(self.R_pre_duty)


#     def __del__(self):
#         self.pwma.stop()
#         self.pwmb.stop()
#         GPIO.cleanup()
