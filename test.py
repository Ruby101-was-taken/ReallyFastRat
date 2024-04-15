import os
os.system("cls")
from jsonParse import *


levelInfo = parseJsonFile(f"levels/levels/1-1.json")

lvl = [[] for i in range(20)]
print(lvl)


print(levelInfo["height"])
for info in levelInfo["layers"][0]["chunks"]:
    print(info["x"])
    #print(f"x: {levelInfo['layers'][0]['chunks'][0]['x']}, y: {levelInfo['layers'][0]['chunks'][0]['y']}")
