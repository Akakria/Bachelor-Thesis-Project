from rpi_hardware_pwm import HardwarePWM
from component import Component
from time import perf_counter

class ServoController(Component):
    """Class for operating servos on the mobile sensor platform"""  
    
    def __init__(self, idleDuty = 7.5, freq = 50) -> None:
        super().__init__()
        self.servoRight = HardwarePWM(pwm_channel=0, hz=freq)
        self.servoLeft = HardwarePWM(pwm_channel=1, hz=freq)
        self.idleDuty: float = idleDuty
        self.executionTime: float = 0.2
        self.lastUpdate: float = perf_counter()
        
        
    def setup(self) -> None:
        """begin PWM"""
        
        self.servoRight.start(self.idleDuty)
        self.servoLeft.start(self.idleDuty)
        print("Servos ready")
        
        
    def clear(self) -> None:
        """Clear PWM, release pwm channels"""
        
        self.servoRight.stop()
        print("PWM 0 stopped")
        self.servoLeft.stop()
        print("PWM 1 stopped")
        
 
    def setServoState(self, state: list = [7.5, 7.5], setIdle = False) -> None:
        """Set duty cycle, [n.n, n.n]"""
        
        if not setIdle:
            self.lastUpdate = perf_counter()
            self.servoRight.change_duty_cycle(state[0])
            self.servoLeft.change_duty_cycle(state[1])
        
        else:
            self.servoRight.change_duty_cycle(self.idleDuty)
            self.servoLeft.change_duty_cycle(self.idleDuty)
        
 
    def getReading(self) -> dict:
        """Read current state of servos"""
        
        dutyCycles: dict = {
            "timestamp": super().getTime(),
            "dutyR" : self.servoRight._duty_cycle,
            "dutyL" : self.servoLeft._duty_cycle
        }

        return dutyCycles