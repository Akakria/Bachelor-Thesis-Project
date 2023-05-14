from datetime import datetime


class Component:
    """Base class for sensors and actuator components"""
    
    def __init__(self) -> None:
        pass
    
    
    def getTime(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    
    def setup(self):
        """Setup Component"""
        raise NotImplementedError("Method not implemented")
    
    
    def clear(self):
        raise NotImplementedError("Method not implemented")
    
    
    def getReading(self):
        raise NotImplementedError("Method not implemented")