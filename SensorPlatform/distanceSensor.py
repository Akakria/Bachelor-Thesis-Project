import RPi.GPIO as GPIO
import time
from component import Component


class DistanceSensor(Component):
    """Distance sensor class for HC-SR04 module"""
    
    def __init__(self, trig = 17, echo = 22) -> None:
        super().__init__()
        self.trig: int = trig
        self.echo: int = echo
        
    
    def setup(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        
        
    def clear(self) -> None:
        GPIO.cleanup(self.trig)
        GPIO.cleanup(self.echo)
        
    
    def getReading(self, msg = None) -> float:
        """Get distance reading in cm"""
        
        time.sleep(0.05)  # sensor settle
        
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
        
        initialTime: float = time.time()  # Track the initial time
        timeout: float = 0.04  # Maximum range for HC-SR04 is 4m. 4m / 343m/s = ~0.0116s, so 0.04s is a safe timeout
        
        # Save start time
        while GPIO.input(self.echo) == 0:
            startTime = time.time()
            if startTime - initialTime >= timeout:  # Use the initial time for the timeout check
                return None  # Timeout, return None

        # Save time of arrival
        while GPIO.input(self.echo) == 1:
            stopTime = time.time()
            if stopTime - initialTime >= timeout:  # Use the initial time for the timeout check
                return None  # Timeout, return None

        timeElapsed: float = stopTime - startTime
        distance: float = (timeElapsed * 34300) / 2

        if msg:
            return {"timestamp": super().getTime(),
                    "distance" : distance}
        else:
            return distance