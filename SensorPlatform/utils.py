import subprocess


def cpuTemperature() -> float:
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as tempFile:
        cpuTempMilli = int(tempFile.read())
        return float(cpuTempMilli / 1000)
    

def terminate(payload) -> None:
    if payload["action"] == 1:
            print("Termination requested")


def shutdown(debug=False) -> None: #TODO: implement cmdline arguments
    if not debug:
        subprocess.run(["sudo", "shutdown", "-h", "now"])
    else:
        print("exit program")