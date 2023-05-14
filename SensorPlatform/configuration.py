class Configuration(): #TODO: implement remote config
    def __init__(self) -> None:
        self.trigPin = 17
        self.echoPin = 22
        self.freq = 50
        self.idle = 7.5
        self.username = "piBot"
        self.password = "sopaxkrips"
        self.broker = "192.168.1.113"
        self.port = 1883
        