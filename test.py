import os
os.system("cls")
from jsonParse import *

from tiles import *


levelInfo = parseJsonFile(f"levels/levels/1-1.json")

lvl = [[] for i in range(20)]
print(lvl)


print(levelInfo["height"])
for info in levelInfo["layers"][0]["chunks"]:
    print(info["x"])
    #print(f"x: {levelInfo['layers'][0]['chunks'][0]['x']}, y: {levelInfo['layers'][0]['chunks'][0]['y']}")
    
    
    
testMap = {}

print(True if "Joe" in testMap else False)


testMap["Joe"] = {int: 100}


print(True if "Joe" in testMap else False)


print(testMap["Joe"][int])


testTile = createTile(0, 1, 0)
testTile2 = createTile(0, 1, 16)


print(type(testTile) == type(testTile2))