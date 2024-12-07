import os
from scripts.jsonParse import *



class HatManager:
    def __init__(self):
        self.path = "data/hats.json"
        self.hoveredHat = "none"
        
    def loadHats(self):
        if not os.path.isfile(self.path):
            dictToJson(self.path, {"hats":[]})
            return
        
        self.hats = parseJsonFile(self.path)
        for hat in self.hats["hats"]:
            self.addHatToMenu(hat)
            
    def addHatToMenu(self, hat):
        self.gameManager.addHat(hat)
        
    def unlockHat(self, hat):
        if not hat in self.hats["hats"]:
            self.hats["hats"].append(hat)
            self.hats["hats"] = sorted(self.hats["hats"])
            self.saveHats()
            self.addHatToMenu(hat)
        
    def saveHats(self):
        dictToJson(self.path, self.hats)
        
hatManager = HatManager()