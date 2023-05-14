import json
from utils import MQTT, TOPICS
import paho.mqtt.client as mqtt


class MqttClient():
    def __init__(self, log, ui) -> None:
        self.client = mqtt.Client(userdata = TOPICS)
        self.client.username_pw_set(MQTT["username"], MQTT["password"])
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.log = log
        self.ui = ui
        self.client.connect(MQTT["broker"], int(MQTT["port"]), 60)
        self.client.loop_start()
        
        
    def publish(self, topic, payload, qos = 0) -> None:
        msg = json.dumps(payload)
        self.client.publish(topic, msg, qos=qos)


    def onConnect(self, client, userdata, flags, rc):
        print(f"Connected to broker with code {rc}")
        
        for topic in userdata["responses"].values():
            client.subscribe(topic)
    
    
    def onMessage(self, client, userdata, msg):
        topic = msg.topic
        payload = json.loads(msg.payload.decode("utf-8"))

        if topic == userdata["responses"]["sensors"]:
            self.log(data=payload)
            self.ui(payload)
            
        else:
            print(f"message to {msg} to {topic}")   
            
            
    def disconnect(self):
        print("client disconnecting from broker...")
        self.client.disconnect()
        self.client.loop_stop()   
        print("disconnected")

