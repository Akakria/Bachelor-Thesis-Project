from utils import setCursorPosition
import os

class UserInterface():
    
    def __init__(self) -> None:
        self._data: dict = {}


    def updateUI(self, data = None) -> None:
        if data:
            self._data.update(data)
        self.printUI(isUpdate=True)

                
    def printUI(self, isUpdate: bool = False):
        
        if isUpdate:
            setCursorPosition(0,4)
            for key, value in self._data.items():
                if type(value) == float:
                    print("{:<15}{:,.2f}".format(key + ":", value))
                else:
                    print("{:<15}{}".format(key + ":", value))
        
        else:
            os.system('cls' if os.name=='nt' else 'clear')
            print(f"""SENSOR PLATFORM OPERATOR INTERFACE\nServos: Arrow keys\nSensors: Environment(F1)\nData:\n""")
        
    
        

     
        
