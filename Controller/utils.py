from configparser import ConfigParser
import ctypes
import socket

#config
config = ConfigParser()
config.read("configuration.ini")

MQTT=  dict(config["mqtt"])

TOPICS =\
{
    "actions"   : dict(config["actions"]),
    "responses" : dict(config["responses"])
}   

DUTY = {k: tuple(map(float, v.split(", "))) for k, v in config["duty"].items()}

VIDEO = dict(config["video"])


def getIp():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    return host_ip


#cmdln functions 
def setCursorPosition(x, y):
    """Move cursor to position x,y in command prompt"""
    try:
        hConsole = ctypes.windll.kernel32.GetStdHandle(-11)
        position = ctypes.c_ulong((y << 16) | x)
        ctypes.windll.kernel32.SetConsoleCursorPosition(hConsole, position)
    except:
        print("Invalid terminal")
