
class PID:
    """PID Controller
    """

    def __init__(self, P=80, I=0, D=0, duty=26):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.err_pre = 0
        self.err_last = 0
        self.u = 0
        self.integral = 0
        self.last_duty = duty
        self.pre_duty = duty


    def update(self, err):
        self.err_pre = err
        self.integral+= self.err_pre
        self.u = self.Kp*self.err_pre + self.Ki*self.integral + self.Kd*(self.err_pre-self.err_last)
        self.err_last = self.err_pre
        self.pre_duty = self.last_duty + self.u
        if self.pre_duty > 100:
            self.pre_duty = 100
        elif self.pre_duty < 0:
            self.pre_duty = 0
        self.last_duty = self.pre_duty
        return self.pre_duty
