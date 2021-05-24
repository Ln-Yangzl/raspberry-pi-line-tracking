import time
import RPi.GPIO as GPIO
import threading
from pid import PID


EA, I2, I1, EB, I4, I3, LS, RS = (13, 19, 26, 16, 20, 21, 6, 12)
FREQUENCY = 50

class directionControler:

    def __init__(self, LP, LI, LD, L_init_duty, RP, RI, RD, R_init_duty, target_duty = 80):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
        GPIO.setup([LS, RS],GPIO.IN)
        GPIO.output([EA, I2, EB, I3], GPIO.LOW)
        GPIO.output([I1, I4], GPIO.HIGH)
        self.pwma = GPIO.PWM(EA, FREQUENCY)
        self.pwmb = GPIO.PWM(EB, FREQUENCY)
        self.pwma.start(0)
        self.pwmb.start(0)
        self.L_control = PID(LP, LI, LD, L_init_duty)   # for pwma
        self.R_control = PID(RP, RI, RD, R_init_duty)   # for pwmb
        self.ideal_duty = target_duty
        self.L_pre_duty = L_init_duty
        self.R_pre_duty = R_init_duty


    def update(self, loss):
        if loss > 0:
            if self.L_pre_duty < self.ideal_duty:
                self.L_pre_duty = self.L_control.update(loss)
            else:
                self.R_pre_duty = self.R_control.update(loss)
        elif loss < 0:
            if self.L_pre_duty > self.ideal_duty:
                self.L_pre_duty = self.L_control.update(loss)
            else:
                self.R_pre_duty = self.R_control.update(loss)
        self.pwma.ChangeDutyCycle(self.L_pre_duty)
        self.pwmb.ChangeDutyCycle(self.R_pre_duty)


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
        GPIO.add_event_detect(LS,GPIO.RISING,callback=self.__my_callback)
        GPIO.add_event_detect(RS,GPIO.RISING,callback=self.__my_callback)

    def run(self):
        while True:
            self.rspeed=(self.rcounter/20.00)
            self.lspeed=(self.lcounter/20.00)
            self.rcounter = 0
            self.lcounter = 0
            time.sleep(0.1)

    def speedLoss(self):
        return self.rspeed - self.lspeed

    def __my_callback(self, channel):
        if (channel==LS):
            self.lcounter+=1
        elif(channel==RS):
            self.rcounter+=1

    def __del__(self):
        GPIO.cleanup()