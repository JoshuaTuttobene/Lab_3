class ClosedLoop_P:

    def __init__ (self, Kp,setpoint):
        self.kp = Kp
        self.setpoint = setpoint
    
    def run(self,position):
        self.position = position
        pwm = Kp*(self.setpoint-self.position)
        return pwm
    
    def set_setpoint(self,setpoint):
        self.setpoint = setpoint
        return print('setpoint:',self.setpoint)
    
    def set_kp(self,kp):
        self.kp = kp
        return print('Kp:',self.kp)