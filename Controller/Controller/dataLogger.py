import os
import csv

class DataLogger():
    def __init__(self) -> None:
        self.folder = "Logs"
        self.fileName = "sensorLog.csv"
    
    
    def logData(self, data: dict = None) -> None:
        try:
            self.writeDictToCsv(data)
            
        except Exception as e: print(e)
    
    
    def writeDictToCsv(self, dataDict: dict) -> None:
        """Write the values to the CSV file """
        
        # Create the folder if it doesn't exist
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        folderPath = os.path.join(scriptDir, self.folder)

        # Create the folder if it doesn't exist
        os.makedirs(folderPath, exist_ok=True)

        # Create the CSV file if it doesn't exist and write the headers
        filePath = os.path.join(folderPath, self.fileName)
        fileExists = os.path.isfile(filePath)
        with open(filePath, mode='a', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=dataDict.keys())
            if not fileExists:
                writer.writeheader()

            # Write the values to the CSV file
            writer.writerow(dataDict)