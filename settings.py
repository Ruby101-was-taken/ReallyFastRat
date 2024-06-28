import os
from jsonParse import *

class Settings:
    def __init__(self) -> None:
        self.defaults = {
            "musicVolume": 100,
            "sfxVolume": 100,
            "backgroundDetail": 2,
            "animatedTile": True,
            "animateTilesAtSpeed": False,
            "simpleUI": False,
            "particles": True
        }
        self.loadSettings()
        
    def resetSettings(self):
        dictToJson("settings.json", self.defaults)
        
    def updateSettings(self):
        dictToJson("settings.json", self.settings)
        
    def loadSettings(self):
        if not os.path.isfile("settings.json"):
            self.resetSettings()
        
        self.settings = parseJsonFile("settings.json")
        
        if self.settings.keys() == self.defaults.keys():
            print("settings are valid")
        else:
            print("resetting settings D:")
            self.resetSettings()
            
    def increaseMusicVolume(self):
        self.settings["musicVolume"] += 5
        if self.settings["musicVolume"] > 100: self.settings["musicVolume"] = 100
    def decreaseMusicVolume(self):
        self.settings["musicVolume"] -= 5
        if self.settings["musicVolume"] < 0: self.settings["musicVolume"] = 0
        
    def toggleBG(self):
        self.settings["backgroundDetail"]-=1
        if self.settings["backgroundDetail"] == -1: self.settings["backgroundDetail"] = 2
            
s = Settings()