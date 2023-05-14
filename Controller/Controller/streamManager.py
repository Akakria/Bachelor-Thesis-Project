import subprocess


class StreamManager:
    def __init__(self, ip, port=5000):
        self.port = port
        self.ip = ip
        self.framerate = 15
        self.process = None
        self.streamParams = f"libcamera-vid -t 0 --framerate {self.framerate} --width 640 --height 480 --codec h264 --output - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host={self.ip} port={self.port}"
        self.data = {"data" : self.streamParams,
                     "action" : None}
    
    def startStream(self):
        if not self.process:
            cmd = f'gst-launch-1.0 -v udpsrc port={self.port} ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false'
            self.process = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
    
    def stopStream(self):
        if self.process:
            print("stream terminate")
            self.process.terminate()
            self.process = None