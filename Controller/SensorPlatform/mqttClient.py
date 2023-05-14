import paho.mqtt.client as mqtt
import json
from utils import terminate


class MqttClient(): 
    def __init__(self, duty, sensors, stream, config, terminationEvent, terminate = terminate) -> None: 
        self.actions =\
        {
                "operator/action/duty" : duty,
                "operator/action/sensors": sensors,
                "operator/action/stream": stream,
                "operator/action/terminate": terminate,
                "operator/lwt": terminate
        }
        self.responses = "platform/response/sensors"
 
        self.terminationEvent = terminationEvent
        self.client = mqtt.Client(userdata=config)
        self.client.username_pw_set(config.username, config.password)
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(config.broker, config.port)
        self.client.loop_start()
        
        #TODO: implement dynamic topics, i.e. operator dictates topics
      
    
    def publish(self, topic, payload):
        msg = json.dumps(payload)
        self.client.publish(topic, msg)
    
    
    def onConnect(self, client, userdata, flags, rc):
        print(f"Connected to broker with code {rc}")
        
        for topic in self.actions.keys():
            client.subscribe(topic)
            
  
    def onMessage(self, client, userdata, msg):
        topic = msg.topic
        payload = json.loads(msg.payload.decode("utf-8")) 
        action = self.actions[topic](payload)  
        
        if topic == "operator/action/terminate" and payload["action"] == 1:
            self.terminationEvent.set()
 
        if action: #TODO: implement multiple response topics handling
            self.publish(self.responses, action)
            
    
    def disconnect(self): #TODO: implement Last will and testament
        print("client disconnecting from broker...")
        self.client.disconnect()
        self.client.loop_stop()   
        print("disconnected")