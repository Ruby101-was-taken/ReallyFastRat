import json
import copy

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
        
def combineDict(og, new) -> dict:
    newDict = copy.copy(og)
    for key, value in new.items():
        newDict[key] = value
    
    return newDict

def parseJsonFileWithBase(filePath: str, base) -> dict:
    if isinstance(base, str):
        baseDict = parseJsonFile(base)
    elif isinstance(base, dict):
        baseDict = base
    else:
        return parseJsonFile(filePath)
    
    return combineDict(baseDict, parseJsonFile(filePath))

    
