import os
from scripts.jsonParse import *

class Settings:
    def __init__(self) -> None:
        self.defaults = {
            "musicVolume": 50,
            "sfxVolume": 100,
            "backgroundDetail": 2,
            "animatedTile": True,
            "animateTilesAtSpeed": False,
            "simpleUI": False,
            "particles": True,
            "drawOnThread": False,
            "bgType": "city",
            "hwaccel": False,
            "quickRestartButton": True,
            "hat": "none"
        }
        self.loadSettings()
        
    def resetSettings(self):
        dictToJson("data/settings.json", self.defaults)
        
    def updateSettings(self):
        dictToJson("data/settings.json", self.settings)
        
    def loadSettings(self):
        if not os.path.isfile("data/settings.json"):
            self.resetSettings()
        
        self.settings = parseJsonFile("data/settings.json")
        
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
        
    def toggleDrawThread(self):
        self.settings["drawOnThread"] = not self.settings["drawOnThread"]
        
    def toggleParticles(self):
        self.settings["particles"] = not self.settings["particles"]
        
    def toggleQuickRestart(self):
        self.settings["quickRestartButton"] = not self.settings["quickRestartButton"]
        
        
    def increaseSoundVolume(self):
        self.settings["sfxVolume"] += 5
        if self.settings["sfxVolume"] > 100: self.settings["sfxVolume"] = 100
    def decreaseSoundVolume(self):
        self.settings["sfxVolume"] -= 5
        if self.settings["sfxVolume"] < 0: self.settings["sfxVolume"] = 0
            
s = Settings()