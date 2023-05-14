import time
import traceback
import threading
from utils import shutdown
from configuration import Configuration
from servoController import ServoController
from distanceSensor import DistanceSensor
from senseHatWrapper import SenseHatWrapper
from mqttClient import MqttClient
from streamManager import StreamManager

   
def main():
    
    terminationEvent = threading.Event() #deals with thread termination
    streamManager = StreamManager() #manages GStreamer subprocess
    config = Configuration() #program configuration
    
    senseHatWrapper = SenseHatWrapper() 
    senseHatWrapper.setup()
    
    senseHatWrapper.setStatusLED("yellow") #status light (setting up, connecting etc,)
    
    servoController = ServoController(config.idle, config.freq)
    servoController.setup()
    
    distanceSensor = DistanceSensor(config.trigPin, config.echoPin)
    distanceSensor.setup()
    
    mqttClient = MqttClient(servoController.setServoState, #mqtt client setup, takes methods for message callbacks
                            senseHatWrapper.getReading,
                            streamManager.streamToggle,
                            config,
                            terminationEvent)
    
    senseHatWrapper.setStatusLED("green") #setup done
    
    def terminate() -> None: #lazy nested function to deal with program termination
        print("Terminating...")
        senseHatWrapper.clear()
        servoController.clear()
        distanceSensor.clear()
        streamManager.streamToggle(None)
        mqttClient.disconnect()
        print("...Done")
        shutdown(debug=True)    
    
    try:
        while not terminationEvent.is_set(): # "main loop", 
            if time.perf_counter() - servoController.lastUpdate >= servoController.executionTime:
                servoController.setServoState(setIdle = True)
                
            senseHatWrapper.setProximityLED(distanceSensor.getReading())
            senseHatWrapper.btnTerminate()
            
            time.sleep(0.05) 
    
    except: 
        traceback.print_exc() 
        senseHatWrapper.setStatusLED("red")
        terminate()
        
    finally:
        terminate()
    
    terminate()

if __name__ == "__main__":
    main()
    