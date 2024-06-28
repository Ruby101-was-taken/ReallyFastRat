import json

def parseJsonFile(filePath):
    try:
        with open(filePath, 'r') as jsonFile:
            data = json.load(jsonFile)
            return data
    except json.JSONDecodeError as e:
        return {}
    
def dictToJson(filename, dictionary):
    with open(filename, "w") as file:
        json.dump(dictionary, file, indent=4)
        
    
