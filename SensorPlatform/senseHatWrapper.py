from sense_hat import SenseHat
from component import Component
from utils import cpuTemperature


class SenseHatWrapper(Component):
    """wrapper for sense hat"""
    
    def __init__(self) -> None:
        super().__init__()
        self.sense: SenseHat = self.setup()
        self.ledBrightness: int = 100
    
    
    def setup(self) -> SenseHat:
        """Init SenseHAT"""
        return SenseHat()
    
    
    def clear(self) -> None:
        """Clear LED matrix"""
        self.sense.clear()
        
    
    def btnTerminate(self) -> None:
        """Terminate program via SenseHAT button"""
        events = self.sense.stick.get_events()
        if events:
            for event in events:
                if event.action == 'pressed':
                    print("Terminate pressed...")
                    raise Exception


    def setStatusLED(self, color) -> None:
        """Set status light state"""
        
        self.sense.clear()
        if color == "yellow":
            r, g, b = self.ledBrightness, self.ledBrightness, 0
        elif color == "green":
            r, g, b = 0, self.ledBrightness, 0
        elif color == "red":
            r, g, b = self.ledBrightness, 0, 0
        else:
            r, g, b = 0, 0, 0  # Off

        indices = [(3, 3), (3, 4), (4, 3), (4, 4)]

        for x, y in indices:
            self.sense.set_pixel(x, y, r, g, b)
    
    
    def setProximityLED(self, proximity) - None:
        """Set proximity light state"""
        
        leds = self.sense.get_pixels()

        # Determine the color based on the proximity value
        if proximity < 10:
            r, g, b = self.ledBrightness, 0, 0  # Red
        elif proximity < 20:
            r, g, b = self.ledBrightness, self.ledBrightness, 0  # Yellow
        else:
            r, g, b = 0, self.ledBrightness, 0  # Green

        for y in range(8):
            self.sense.set_pixel(0, y, r, g, b)
            self.sense.set_pixel(1, y, r, g, b)

      
    def getReading(self, data) -> dict:
        """Get Environmental sensor readings"""
        
        cpu: float = cpuTemperature()
        temperature: any = self.sense.get_temperature()
        humidity: any = self.sense.get_humidity()
        pressure: any = self.sense.get_pressure()
        
        return {"timestamp" :   super().getTime(),
                "cpu":          cpu,
                "temperature":  temperature, 
                "humidity":     humidity, 
                "pressure":     pressure}
    
    

    