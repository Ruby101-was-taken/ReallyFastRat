import json

def parseJsonFile(filePath):
    with open(filePath, 'r') as jsonFile:
        data = json.load(jsonFile)
        return data