from keyboard import get_hotkey_name
from utils import TOPICS, DUTY
import threading
import time

class InputProcessor():
    """Process keyboard input"""

    def __init__(self, publish, stopEvent, streamManager) -> None:
        self.topics = TOPICS["actions"]
        self.duty = DUTY
        self.publish = publish
        self.stopEvent = stopEvent
        self.streamManager = streamManager
        self.inputThread = threading.Thread(target=self.eventListener)
        self.inputThread.daemon = True
        self.inputThread.start()
  

    def processEvent(self, key) -> None:
        """Process keyboard input and return correct topic and command"""
        match key:
            case "ylänuoli": #key names depend on settings, cant put these in config, because irrefutable patterns are not allowed ¯\_(ツ)_/¯
                self.publish(self.topics["movement"], self.duty["forward"])
            case "oikea nuoli":
                self.publish(self.topics["movement"], self.duty["right"])
            case "alanuoli":
                self.publish(self.topics["movement"], self.duty["backward"])
            case "vasen nuoli":
                self.publish(self.topics["movement"], self.duty["left"])
                
            case "f1":
                self.publish(self.topics["sensors"], 1)
            case "f2":
                self.streamManager.data["action"] = "start"
                self.publish(self.topics["stream"], self.streamManager.data, 2)
                self.streamManager.startStream()
            case "f3":
                self.streamManager.data["action"] = "stop"
                self.publish(self.topics["stream"], self.streamManager.data, 2)
                self.streamManager.stopStream()
            case "f4":
                self.publish(self.topics["terminate"], {"data": "", "action" : 1}, 2)
                
            case "f5": 
                self.publish(self.topics["movement"], self.duty["idle"])
            case "esc":
                self.stopEvent.set()


    def eventListener(self) -> None:
        """key event callback"""
        while not self.stopEvent.is_set():
            key = get_hotkey_name().split("+")[-1]
            self.processEvent(key)
            time.sleep(0.1)  # Prevent busy-waiting