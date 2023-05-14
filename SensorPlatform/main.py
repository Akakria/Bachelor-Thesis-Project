import time
import traceback
import threading
from utils import terminate, shutdown
from configuration import Configuration
from servoController import ServoController
from distanceSensor import DistanceSensor
from senseHatWrapper import SenseHatWrapper
from mqttClient import MqttClient
from streamManager import StreamManager

   
def main():
    terminationEvent = threading.Event()
    streamManager = StreamManager()
    config = Configuration()
    
    senseHatWrapper = SenseHatWrapper()
    senseHatWrapper.setup()
    
    senseHatWrapper.setStatusLED("yellow")
    
    servoController = ServoController(config.idle, config.freq)
    servoController.setup()
    
    distanceSensor = DistanceSensor(config.trigPin, config.echoPin)
    distanceSensor.setup()
    
    mqttClient = MqttClient(servoController.setServoState, 
                            senseHatWrapper.getReading,
                            streamManager.streamToggle,
                            terminate,
                            config,
                            terminationEvent)
    
    senseHatWrapper.setStatusLED("green")
    
    def terminate():
        print("Terminating...")
        senseHatWrapper.clear()
        servoController.clear()
        distanceSensor.clear()
        streamManager.streamToggle(None)
        mqttClient.disconnect()
        print("...Done")
        shutdown(debug=True)    
    
    try:
        while not terminationEvent.is_set():
            if time.perf_counter() - servoController.lastUpdate >= servoController.executionTime:
                servoController.setServoState(setIdle = True)
                
            senseHatWrapper.setProximityLED(distanceSensor.getReading())
            senseHatWrapper.btnTerminate()
            
            time.sleep(0.05) 
    
 
    
    except: 
        traceback.print_exc() 
        senseHatWrapper.setStatusLED("red")
        terminate(None)
        
    finally:
        terminate()


if __name__ == "__main__":
    main()
    