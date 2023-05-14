from inputProcessor import InputProcessor
from userInterface import UserInterface
from mqttClient import MqttClient
from dataLogger import DataLogger
from streamManager import StreamManager
from time import sleep
import threading


def main() -> None:
    """Controller driver code"""
    stopEvent = threading.Event()
    
    try:
        interface = UserInterface()
        logger = DataLogger()
        mqttClient = MqttClient(logger.logData, interface.updateUI)
        streamManager = StreamManager("192.168.1.113")
        inputProcessor = InputProcessor(mqttClient.publish, stopEvent, streamManager)
        interface.printUI()


        while not stopEvent.is_set():  
            sleep(1) 
            
    except KeyboardInterrupt:
        print("Interrupted")
        stopEvent.set()
        
    except Exception as e:
        print(e)
        stopEvent.set()
        
    finally:
        print("cleanup")
        mqttClient.disconnect()
        
            
if __name__ == "__main__":
    main()

