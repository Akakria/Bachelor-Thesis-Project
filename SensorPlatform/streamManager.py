import os
import signal
import subprocess

class StreamManager():
    def __init__(self) -> None:
        self.process = None

    def streamToggle(self, payload = {"data": None, "action": None}) -> None:
        action = payload["action"]
        data = payload["data"]
        

        if self.process and action == "stop":
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)  # Send the signal to all the process groups
            self.process = None
            print("stopped stream")

        elif not self.process and action == "start":
            self.process = subprocess.Popen(data, shell=True, preexec_fn=os.setsid)  # Starts the process in a new process group
