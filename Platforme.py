

worldX, worldY = 1,0

collisionTiles = 0



import pygame, random, os, csv, copy, time, sys
import math as maths
import webbrowser

from animation import Animation

from audioSource import AudioSource

from colours import *

from ratFacts import facts

from scripts.jsonParse import *
from generalMaths import *

from settings import s
from scripts.hatLoader import hatManager

from Camera import Camera


from profiler import *

import pygame._sdl2 as pg_sdl2

from Background import Background 


from Particle import *
from scripts.decal import Decal


os.system("cls")


useFullScreen = True # change to load on fullscreen or not

# Set win dimensions
w = 1280
h = 720


tileSize = 20  

borderW = 50


#bg have 5 colours btw


# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

window = pygame.display.set_mode((w, h), pygame.SCALED | pygame.HIDDEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
coolerWindow = pygame.Window.from_display_module()  # these
#coolerWindow.set_fullscreen(useFullScreen)  # three
coolerWindow.show()  # lines :)

coolerWindow.resizable = True
    
    
from resources import resources #load all images from the external python file
from entity import Entity

from scripts.tiles.tiles import *
from scripts.tiles.createTile import createTile
from object import Object

class noJoystick:
    def get_init(self):
        return False
    def get_button(self, num):
        return False
    def get_axis(self, num):
        return False
    def get_hat(self, num):
        return (0,0)
    def init(self):
        print("nice try")

def reloadController():
    global joystick, win
    num_joysticks = pygame.joystick.get_count()
    if num_joysticks > 0:
        if num_joysticks == 1:
            joystick = pygame.joystick.Joystick(0)
            joystick.rumble(1, 1, 1000)
        else:
            from extraControllers import getController
            joystick = pygame.joystick.Joystick(getController(num_joysticks, pygame.joystick))
            joystick.rumble(1, 1, 1000)
            pygame.display.set_caption("Really Fast Rat")
        joystick.init()
        try:
            debugLog.append(DebugLogText(f"{joystick.get_name()} connected!", 240, "controller"))
        except NameError:
            print(joystick.get_name())
    else:
        try:
            debugLog.append(DebugLogText("No Controllers Detected. Reconnect it and try again.", 240, "warning"))
        except NameError:
            print("No Controller")
        joystick = noJoystick()
        
reloadController()

isXboxController = False
if joystick.get_init():
    if "xbox" in joystick.get_name().lower():
        isXboxController = True


    
pygame.display.set_caption("Really Fast Rat")
pygame.display.set_icon(pygame.image.load('ui/icon.png'))

logo=[pygame.image.load('logo/logosubless.png'), pygame.image.load('logo/logoSUB.png'), pygame.image.load('logo/logoDecorSmol.png')]




loadingTexts = ["LOADING IMAGES", "LOADING UI", "LOADING SOUNDS"]


# Set up fonts
smallFont = pygame.font.SysFont("arial", 20)
smallerFont = pygame.font.SysFont("arial", 15)
bigFont = pygame.font.SysFont("arial", 45)

loadingFactFont = pygame.font.SysFont("arial", 30)


def quitGame():
    pygame.quit()
    sys.exit()

# Set up timer
clock = pygame.time.Clock()

win = pygame.Surface((w, h))


#region logo
logoPos = 0
logoSubPos = pygame.math.Vector2()
logoSubPos.x = -401
logoSubPos.y = h+146


showLogo:bool = True
run:bool = True

if showLogo:
    logoScreen = True
    delay = 60
    while logoScreen and run:
        win.fill(LOGORED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.VIDEORESIZE:
                # This event is triggered when the win is resized
                w, h = event.w, event.h
        delay-=1
        if delay <= 0:
            if logoPos < 473:
                logoPos = pygame.math.lerp(logoPos, 473, 0.05)
            win.blit(logo[0], (logoPos, 313))
        if delay <= -60:
            if logoSubPos.x < 511 and logoSubPos.y > 318:
                logoSubPos.x = pygame.math.lerp(logoSubPos.x, 511, 0.05)
                logoSubPos.y = pygame.math.lerp(logoSubPos.y, 318, 0.045)
            win.blit(logo[1], logoSubPos)
            
        logoScreen = delay > -400
        window.blit(win, (0,0)) 
        pygame.display.flip()

    del delay, logoScreen, logoPos, logoSubPos


if not run:
    quitGame()
    
#endregion logo


def resliceImages(tileType:str):
    tileImages.groundImages = resources.sliceTilemap(pygame.image.load(f"levelAssets/tileMap/{tileType}/ground.png").convert_alpha(), tileSize, tileSize)
    tileImages.spikeImages = resources.sliceTilemap(pygame.image.load(f"levelAssets/tileMap/{tileType}/spikeTiles.png").convert_alpha(), tileSize, tileSize)
    tileImages.bridgeImages = resources.sliceTilemap(pygame.image.load(f"levelAssets/tileMap/{tileType}/bridgeTiles.png").convert_alpha(), tileSize, tileSize)
    tileImages.objectImages = resources.sliceTilemap(pygame.image.load(f"levelAssets/tileMap/{tileType}/objectTiles.png").convert_alpha(), tileSize, tileSize)
    tileImages.groundBImages = resources.sliceTilemap(pygame.image.load(f"levelAssets/tileMap/{tileType}/groundB.png").convert_alpha(), tileSize, tileSize)
    tileImages.groundCImages = resources.sliceTilemap(pygame.image.load(f"levelAssets/tileMap/{tileType}/groundC.png").convert_alpha(), tileSize, tileSize)
    tileImages.groundDImages = resources.sliceTilemap(pygame.image.load(f"levelAssets/tileMap/{tileType}/groundD.png").convert_alpha(), tileSize, tileSize)

    tileImages.backGroundAImages = resources.sliceTilemap(pygame.image.load(f"levelAssets/tileMap/{tileType}/backGroundA.png").convert_alpha(), tileSize, tileSize)
    tileImages.backGroundBImages = resources.sliceTilemap(pygame.image.load(f"levelAssets/tileMap/{tileType}/backGroundB.png").convert_alpha(), tileSize, tileSize)
    tileImages.backGroundCImages = resources.sliceTilemap(pygame.image.load(f"levelAssets/tileMap/{tileType}/backGroundC.png").convert_alpha(), tileSize, tileSize)
    tileImages.backGroundDImages = resources.sliceTilemap(pygame.image.load(f"levelAssets/tileMap/{tileType}/backGroundD.png").convert_alpha(), tileSize, tileSize)
    
    tileImages.movingPlatformImages = resources.sliceTilemap(pygame.image.load(f"levelAssets/tileMap/{tileType}/movingPlatform.png").convert_alpha(), tileSize, tileSize)


resliceImages("Test")


win.blit(smallFont.render(loadingTexts[0] + " - COMPLETED", True, (255, 255, 255)), (0,200+(0*20)))
pygame.display.flip()

#load ui text
win.blit(smallFont.render(loadingTexts[1], True, (255, 255, 255)), (0,200+(1*20)))
pygame.display.flip()
ui = {
}

win.blit(smallFont.render(loadingTexts[1] + " - COMPLETED", True, (255, 255, 255)), (0,200+(1*20)))
pygame.display.flip()


#load sounds text
win.blit(smallFont.render(loadingTexts[2], True, (255, 255, 255)), (0,200+(2*20)))
pygame.display.flip()
sound = {
}

win.blit(smallFont.render(loadingTexts[1] + " - COMPLETED", True, (255, 255, 255)), (0,200+(2*20)))
pygame.display.flip()


pygame.time.delay(100)


deltaTime = 1



defaultKTime = 10

# Set up fonts
font = pygame.font.Font(None, 36)
smallFont = pygame.font.SysFont("arial", 20)
smallerFont = pygame.font.SysFont("arial", 15)
bigFont = pygame.font.SysFont("arial", 45)

debugLogFont = pygame.font.Font("ui/fonts/debug.ttf")

# Set up timer
clock = pygame.time.Clock()

win.blit(smallFont.render(loadingTexts[0], True, (255, 255, 255)), (200,200+(0*20)))
pygame.display.flip() 



class GameManager:
    def __init__(self):
        self.reset()
        self.mainMenu = True
        self.inGame = False
        self.settingsMenu = False
        
        self.bgDetailLevels = ["Off", "Min", "Max"]
        
        self.timer = 0
        self.timeString = ""
        
        self.timerOn = False
        
        self.flyMode = False
        
        
        self.collectables = 0
        self.collectablesLast = 0
        self.collectablesForNextLevel = 20
        
        self.camera = Camera(0,0)
        self.camXLim = 0
        self.camYLim = 0
        self.camXMin = 0
        self.camYMin = 0
        
        self.particles = []
        
        self.useFullScreen = False
        
        self.showController = joystick.get_init()
        
        self.lastHat = "none"
        
        hatManager.gameManager = self
        self.hoveredHat = "none"
        
    def update(self):
        
        
        if self.collectablesLast != self.collectables:
            if self.collectables >= self.collectablesForNextLevel:
                self.collectables = 0
                player.levelUp()
            hud.getElementByTag("coins").updateText(f"Coins: {self.collectables}/{self.collectablesForNextLevel}")
            
        self.collectablesLast = self.collectables
        
        if self.timerOn:
            self.timer+=deltaTime
         # Calculate total seconds
        totalSeconds = self.timer // 60
        lastTimeString = self.timeString
        self.timeString = self.intToTime(int(totalSeconds))
        if self.timeString != lastTimeString:
            hud.getElementByTag("timer").updateText(self.timeString)
        
        if self.flyMode:
            player.superBoostCoolDown = 0
            player.kTime = 10
            
            
        if self.inGame:
            self.camera.setMaxes(self.camXLim, self.camYLim)
            self.camera.setMins(0, 0)
        
    
    def finalUpdate(self):
        level.updateCameraChanges()
        if self.inGame:

            self.camera.setPos(player.x - w/2, player.y-h/2)
            
        self.camera.update()
        
        if uiHat.show:
            self.updateHatPreview()
        
        
    def addParticle(self, p):
        if s.settings['particles']:
            self.particles.append(p)
            p.gameManager = self
            
    def drawParticles(self, win):
        for p in self.particles:
            p.draw(win, deltaTime)
            
        
    def intToTime(self, num, includeCenti = True) -> str: 
        # Calculate minutes and remaining seconds
        minutes = int(num // 60)
        seconds = int(num % 60)
        
        # Calculate centiseconds
        if includeCenti: centiseconds = (self.timer % 60) * 100 // 60
        else: centiseconds = 0
        
        centiseconds = int(centiseconds)
        
        # Format as MM:SS:ss
        return f"{minutes:02}:{seconds:02}.{centiseconds:02}"
        
        
    def reset(self, resetTime=True):
        self.speed = 3
        self.collectables = 0
        self.rareCollectables = 0
        self.pause = False
        if resetTime: self.timer = 0
        
        
    def togglePause(self):
        self.pause = not self.pause
        uiPause.show = self.pause
        hud.show = not self.pause
        uiPauseButtons.show = self.pause
        if self.pause:
            pygame.mixer.Channel(7).pause()
        else:
            pygame.mixer.Channel(7).unpause()
            if uiSettings.show or uiControls.show:
                self.closeSettingPause()
                
    def toggleMainMenu(self):
        self.mainMenu = not self.mainMenu
        uiMainMenu.show = self.mainMenu
    def toggleLevelSelect(self):
        audioPlayer.playSound(resources.sounds["menuChange"])
        audioPlayer.playSound(resources.sounds["rat"])
        self.toggleMainMenu()
        self.inGame = True
        hud.show = True
        level.changeLevel()
    
    def openFeedback(self):
        webbrowser.open("https://forms.gle/Uez6tRceadLUjGgXA") 
        debugLog.append(DebugLogText("Link Opened", 120, "link"))
        
    def returnToMainMenu(self):
        global worldY
        worldY = 0
        uiPauseButtons.show = False
        uiPause.show = False
        hud.show = False
        self.inGame = False
        self.toggleMainMenu()
        uiLevelTitle.show = False
        uiResults.show = False
        pygame.mixer.Channel(7).unpause()
        audioPlayer.playMusic(MusicSource(f"title.wav"), s.settings["musicVolume"]/100)
        
#region OPEN/CLOSE SETTINGS
    
    def openSettings(self):
        self.settingsMenu = True
        
        uiSettings.show = True
        
    def whichCloseSettings(self):
        if self.inGame:
            self.closeSettingPause()
        else:
            self.closeSettingMainMenu()
        
        
    def closeSettings(self):
        self.settingsMenu = False
        uiSettings.show = False
        uiSettings.resetScroll()
        
        debugLog.append(DebugLogText("Settings Saved", 60))
        
        s.updateSettings()
        
        
    def openSettingsMainMenu(self):
        self.toggleMainMenu()
        
        
        self.openSettings()
        
    def closeSettingMainMenu(self):
        self.toggleMainMenu()
        
        audioPlayer.playMusic(MusicSource(f"title.wav"), s.settings["musicVolume"]/100)
        audioPlayer.playSound(resources.sounds["menuChange"])
        audioPlayer.playSound(resources.sounds["rat"])
        
        self.closeSettings()
        
    def openSettingsPause(self):
        uiPauseButtons.show = False
        
        
        self.openSettings()
        
    def closeSettingPause(self):
        uiPauseButtons.show = self.pause
        audioPlayer.playSound(resources.sounds["menuChange"])
        audioPlayer.playSound(resources.sounds["rat"])
        
        uiControls.show = False
        uiControlsXbox.show = False
        
        self.closeSettings()
    
#endregion
        
#region SETTINGS

    #region SOUND SETTINGS
    def changeMusicVolume(self):
        uiSettings.getElementByTag("musicVolume").updateText(f"{s.settings['musicVolume']}%")
        audioPlayer.music.set_volume(s.settings['musicVolume'] /100)
        
                
    def increaseMusicVolume(self):
        s.increaseMusicVolume()
        self.changeMusicVolume()
    def decreaseMusicVolume(self):
        s.decreaseMusicVolume()
        self.changeMusicVolume()
        
    def changeSoundVolume(self):
        uiSettings.getElementByTag("soundVolume").updateText(f"{s.settings['sfxVolume']}%")
        
                
    def increaseSoundVolume(self):
        s.increaseSoundVolume()
        self.changeSoundVolume()
    def decreaseSoundVolume(self):
        s.decreaseSoundVolume()
        self.changeSoundVolume()
    
    #endregion SOUND SETTINGS
    
    def toggleBG(self):
        s.toggleBG()
        uiSettings.getElementByTag("bgDetail").updateText(f"{self.bgDetailLevels[s.settings['backgroundDetail']]}")
        
        
    def toggleDrawThread(self):
        s.toggleDrawThread()
        uiSettings.getElementByTag("threadText").updateText(f"{s.settings['drawOnThread']}")
        
    def toggleParticles(self):
        s.toggleParticles()
        uiSettings.getElementByTag("particleToggleStatus").updateText(f"{'On' if s.settings['particles'] else 'Off'}")
    
        if not s.settings['particles']:
            self.particles = []
            
    def toggleQuickRestart(self):
        s.toggleQuickRestart()
        uiSettings.getElementByTag("quickRestartToggleStatus").updateText(f"{'On' if s.settings['quickRestartButton'] else 'Off'}")
    
    def toggleFullscreen(self):
        self.useFullScreen = not self.useFullScreen
        # Set up the display
        if not self.useFullScreen:
            coolerWindow.set_windowed()
        else:
            coolerWindow.set_fullscreen(False)
            
        uiSettings.getElementByTag("fullscreenToggleStatus").updateText(f"{'On' if self.useFullScreen else 'Off'}")
    
#endregion SETTINGS

#region OPEN/CLOSE CONTROLS
    def whichShowControls(self):
        if self.inGame:
            self.showControlsPauseMenu()
        else:
            self.showControlsMainMenu()
    def whichCloseControls(self):
        if self.inGame:
            self.hideControlsPauseMenu()
        else:
            self.hideControlsMainMenu()
    
    def showControls(self):
        audioPlayer.playSound(resources.sounds["menuChange"])
        audioPlayer.playSound(resources.sounds["rat"])
        uiControls.show = True
        uiControlsXbox.show = self.showController
        uiControlsPC.show = not self.showController
    def hideControls(self):
        audioPlayer.playSound(resources.sounds["menuChange"])
        audioPlayer.playSound(resources.sounds["rat"])
        uiControls.show = False
        uiControlsXbox.show = False
        uiControlsPC.show = False
        
    def toggleControllerVisual(self):
        self.showController = not self.showController
        uiControlsXbox.show = self.showController
        uiControlsPC.show = not self.showController
        
    def showControlsMainMenu(self):
        uiMainMenu.show = False
        
        self.showControls()
    def hideControlsMainMenu(self):
        uiMainMenu.show = True
        
        self.hideControls()
        
    def showControlsPauseMenu(self):
        uiPauseButtons.show = False
        
        self.showControls()
    def hideControlsPauseMenu(self):
        uiPauseButtons.show = True
        
        self.hideControls()
        
        
    def toggleShowQuit(self):
        uiMainMenu.show = not uiMainMenu.show
        uiMainMenuQuit.show = not uiMainMenuQuit.show
        
#endregion OPEN/CLOSE CONTROLS

    def whichOpenHats(self):
        if uiMainMenu.show:
            self.openHatsMainMenu()
            
    def whichCloseHats(self):
        if self.mainMenu:
            self.closeHatsMainMenu()
        
    def openHatsMainMenu(self):
        uiMainMenu.show = False
        self.openHats()
    
    def closeHatsMainMenu(self):
        uiMainMenu.show = True
        self.closeHats()
        
    def openHats(self):
        uiHat.show = True
    
    def closeHats(self):
        uiHat.show = False
        
#region CHANGE LEVEL

    def startLevelChange(self):
        self.closeResults()
        level.changeLevel(True, True)
        uiPause.show = False
        uiPauseButtons.show = False
        
        isInHub = worldY == 0
        
        uiPauseButtons.getElementByTag("Hub Button").locked = isInHub
        uiPauseButtons.getElementByTag("Restart Button").locked = isInHub
        
        hud.getElementByTag("timer").show = not isInHub
        self.timerOn = not isInHub

    def nextLevel(self):
        global worldX, worldY
        worldX = level.levelInfo["nextLevel"]["x"]
        worldY = level.levelInfo["nextLevel"]["y"]
        
        self.startLevelChange()
        
    def goToLevel(self, x, y):
        global worldX, worldY
        worldX = x
        worldY = y
        
        self.startLevelChange()
        
    def goToHub(self):
        global worldY
        worldY = 0
        
        self.startLevelChange()
        
    def closeResults(self):
        uiResults.show = False
        hud.show = True
        
    def quickRestart(self):
        if worldY != 0:
            self.closeResults()
            uiPause.show = False
            uiPauseButtons.show = False
            player.lastSpawn = self.ogSpawn
            level.reloadTiles()
            player.reset(True) 
            self.timerOn = True
            pygame.mixer.Channel(7).unpause()
        
                
    def toggleFlyMode(self):
        self.flyMode = not self.flyMode
        
#endregion CHANGE LEVEL

    def changeHat(self, hat):
        global playerImages, playerHatImages
        uiHat.getElementByTag(player.hat).styles = settingsButtonStyle
        uiHat.getElementByTag(player.hat).style = settingsButtonStyle.styles[0]
        uiHat.getElementByTag(player.hat).setBG(uiHat.getElementByTag(player.hat).style.colour)
        self.player.hat = hat
        uiHat.getElementByTag(player.hat).styles = highlightedHatButtonStyle
        playerImages = resources.reloadPlayerImages(player.hat)
        playerHatImages = playerImages[-1]
        s.settings["hat"] = hat
        s.updateSettings()
        
    def addHat(self, hat):
        newPos = uiHat.getElementByTag(self.lastHat).screenPos if hat!="none" else (100, 150)
        newPos = (newPos[0], newPos[1]+70)
        print(f"{hat}: {hat!=player.hat}")
        uiHat.addElement(UIHatSelect(newPos, hat, self.changeHat, hat, settingsButtonStyle if hat != player.hat else highlightedHatButtonStyle, hatType=hat, onHover=self.hoverHatButton))
        
        # links the new hat button to the map
        uiHat.UIMap.createLink(hat, "none", "down") # creates the loop back to the top
        uiHat.UIMap.createLink("none", hat, "up") # links the bottom to loop around to the top
        uiHat.UIMap.createLink(hat, self.lastHat, "up") # links the hat to the last hat
        uiHat.UIMap.createLink(self.lastHat, hat, "down") # resets the last hat's down to be the current hat
        uiHat.UIMap.createLink(hat, "back", "right") # links the hat to back button
        

        self.lastHat = hat
        
    def unlockHat(self, hat):
        hatManager.unlockHat(hat)
        uiHat.UIMap.createLink()
        
    def hoverHatButton(self, hat):
        self.hoveredHat = hat
        
    def updateHatPreview(self):
        if self.hoveredHat!=hatManager.hoveredHat:
            if self.hoveredHat == "none":
                uiHat.getElementByTag("hatPreview").changeImages([pygame.Surface((0,0))])
                uiHat.getElementByTag("ratPreview").show = True
                uiHat.getElementByTag("ratPreviewLook").show = False
            else:
                newHatImg = pygame.image.load(f"player/hats/{self.hoveredHat}/player.png").convert_alpha()
                uiHat.getElementByTag("hatPreview").changeImages([pygame.transform.scale(newHatImg, (850, 850))])
                uiHat.getElementByTag("ratPreview").show = False
                uiHat.getElementByTag("ratPreviewLook").show = True
            
            hatManager.hoveredHat = self.hoveredHat
        self.hoveredHat = player.hat
        
        
    def getCoin(self):
        barWidth = hud.getElementByTag("boostBarCoins").w
        self.addParticle(OnScreenParticle(player.blitPosX, player.blitPosY, (barWidth-player.blitPosX)/20, (710-player.blitPosY)/20, 20, 20, 20, YELLOW))
    
    

class Player:
    def __init__(self):
        self.semied = False
        self.x = 475
        self.y = 0
        self.xVel = 0
        self.yVel = 0
        self.charRect = pygame.Rect(475, 300, 20, 30)
        self.rectAsSurface = pygame.Surface((20,20))
        self.rectAsSurface.fill((255,0,0))
        self.image = pygame.image.load("player.png")
        
        self.kTime = 0
        self.wallJumpKTime = 0
        self.wallJumpKTimeDirection = 0
        
        self.climbedLastFrame=False
        self.maxSpeed = gameManager.speed
        self.maxBoost = gameManager.speed*3
        self.defaultBoost = self.maxBoost
        self.terminalVelocityY = 17
        self.terminalVelocityX = 40
        self.boostDirection = 0
        self.canBoost = True
        self.decelSpeed = 0.2
        
        self.decelSpeed = 0.2
        self.gravForce = 0.5
        
        self.groundDecelSpeed = 0.2
        self.airDecelSpeed = 0.05
        
        self.superBoost = 5
        
        self.maxBoostCoolDown = 60
        self.superBoostCoolDown = 0
        
        self.superBoostCoolDownCoins = self.maxBoostCoolDown
        self.minCoinCoolDown = 0
        
        self.superBoostCoolDownFull = 0
        
        self.dashInputBuffer = 0

        self.jumpsLeft = 2

        self.stomp = False

        self.conveyorBonus = 0

        self.jumpPower = 11

        self.walkAnimateFrame = 0
        self.climbAnimateFrame = 0
        self.jumpAnimateFrame = 0
        self.isRight = True

        self.homingRange = pygame.Rect(self.charRect.x-240, self.charRect.y-240, 490, 500)
        self.canHomingAttack = True

        self.homeTo = (0,0)
        self.homeRight = False
        self.homeDown = False
        self.homeSpeed = 3
        self.homingCoolDown = 0

        self.powerUps = []
        
        self.lastSpawn = (0,0)
        
        self.wallJumpDelay = 0
        
        self.resetFrame = True
        
        self.touchGround = True
        
        self.bounce = False
        
        self.hat = "none"
        
        self.speedParticleCoolDown = 5
        
        self.animations = {
            "blink": Animation([0, 18, 19, 18], 10, False),
            "look": Animation([0, 20, 21, 21, 21, 21, 21, 21, 20, 0, 18, 19, 18], 10, False),
            "sit": Animation([0, 22, 23, 24, 25, 26, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 22, 23, 24, 0, 18, 19, 18], 10, False),
        }
        
        self.idleAnimationTimer = 120
        self.idleAnimating = False
        
        self.currentIdleAnimation = "blink"
        
        self.speedParticles = []
        
        
        self.lockMovement:bool = False
    def die(self):
        self.reset(False)
        level.reloadTiles()
    def reset(self, resetTime=True):
        self.resetFrame = True
        gameManager.reset(resetTime)
        self.xVel = 0
        self.yVel = 0
        self.homeTo = (0,0)
        level.levelPosx, level.levelPosy = self.lastSpawn[0], self.lastSpawn[1] 
        self.x, self.y = self.lastSpawn[0], self.lastSpawn[1] 
        self.kTime = 0      
        self.powerUps = []   
        self.superBoostCoolDown=0    
        self.superBoostCoolDownCoins=self.maxBoostCoolDown
        self.minCoinCoolDown = 0
        self.isRight = True     
        gameManager.collectables = 0 
        self.lockMovement = False
        try:
            hud.getElementByTag("fullBoostBar").updateSize(200 + (100*abs(self.minCoinCoolDown/self.maxBoostCoolDown)), 20)
        except NameError:
            pass
#region PLAYER MOVEMENT AND PHYSICS      
    def changeX(self, speed): 
        #self.x+=speed
        fullDebugUi.getElementByTag("speed").updateText("Speed: " + str(speed))
        
        walled = False
        velSign = sign(self.xVel)
        
        
        for i in range(int((abs(speed*2)//20))):
            self.x += sign(speed) * 20
            
            level.levelPosx = self.x
            
            
            if level.checkCollision(self.charRect):
                
                walled = self.wallCheck(velSign)
        
        if abs(int(speed)*2)%20 > 0:
            self.x += (int(speed)*2)%(20 * sign(speed))
            
            level.levelPosx = self.x
            
            
            if level.checkCollision(self.charRect):
                
                walled = self.wallCheck(velSign)
        
            
        
        
        if not walled:
            self.walkAnimateFrame += abs(self.xVel)/7
            if self.walkAnimateFrame >= 4:
                self.walkAnimateFrame = 0
            
        else:
            self.walkAnimateFrame = 0

        if self.x < 0:
            self.x = 0
            self.xVel = 0
            self.walkAnimateFrame = 0
        level.levelPosx=self.x
        
    
    def executeWallJump(self, velSign):
        audioPlayer.playSound(resources.sounds["player"]["jump"])
        self.wallJumped = True
        self.yVel = -10
        self.xVel = 10*-velSign
        self.bounce = False
        self.wallJumpKTime = 0
        
        
        
    def wallCheck(self, velSign) -> bool:
        
        movedUp = False
        moveDownBy = 0
        moveBackBy = 0
        
        walled = False
        
        for i in range(max(10, int(abs(self.xVel)))):
            level.levelPosy-=1
            moveDownBy+=1
            if not level.checkCollision(self.charRect) and not movedUp:
                movedUp = True
                break
        
                
        if not movedUp:
            self.killSpeedParticles()
            walled = True
            level.levelPosy+=moveDownBy
            self.xVel = 0
            
            while level.checkCollision(self.charRect):
                self.x-= 1*velSign
                level.levelPosx = self.x

            
            self.wallJumpKTimeDirection = velSign
            self.wallJumpKTime = 10
            if (inputs.inputEvent("Climb")):
                self.bounce = False
                self.yVel = 0
                self.climbedLastFrame=True
                self.kTime = 0

                if inputs.inputEvent("ClimbUp"):
                    self.climbAnimateFrame+=0.2
                    if self.climbAnimateFrame >= 3:
                        self.climbAnimateFrame = 0
                    self.yVel = -3
                    level.levelPosy -= 30
                    level.levelPosx += velSign
                    if not level.checkCollision(self.charRect):
                        self.yVel = -7
                    level.levelPosy += 30
                    level.levelPosx -= velSign
                elif inputs.inputEvent("ClimbDown"):
                    self.yVel = 3 
                else:
                    self.climbAnimateFrame = 0
                    
            
                    
            elif self.yVel >= 0 and self.kTime <= 0:
                self.yVel = 3 
                self.climbedLastFrame=True
                
                    
        
        return walled


    def changeXVel(self, speed, isRight):
        
        
        
        self.wallJumped = False
        
        maxSpeed = self.maxSpeed        
        maxBoost = self.maxBoost
        
        boostButton = inputs.inputEvent("Boost") and level.levelInfo["canRun"] or self.lockMovement
        
        # if boostButton:
        #     maxSpeed = maxBoost
        
        direction = 1 if self.isRight else -1
            
        if not self.stomp:   
            self.isRight = isRight
            if isRight:
                self.xVel += speed *deltaTime
                if self.xVel > maxSpeed and not (boostButton or self.homeTo!=(0,0)):
                    self.xVel -= speed *deltaTime
                    if self.xVel > maxSpeed:
                        self.xVel-=self.decelSpeed *deltaTime 
                        
                    if self.xVel < maxSpeed: #brings you back to speed if you decelerate too much
                        self.xVel = maxSpeed
                        
                elif self.xVel > maxBoost  and (boostButton or self.homeTo!=(0,0)):
                    self.xVel -= speed *deltaTime
                    if self.xVel > maxBoost :
                        self.xVel-=self.decelSpeed *deltaTime
                    
                    if self.xVel < maxBoost: #brings you back to speed if you decelerate too much
                        self.xVel = maxBoost
                    
                    
                        
            elif not isRight:
                self.xVel -= speed *deltaTime
                if self.xVel < -maxSpeed  and not (boostButton or self.homeTo!=(0,0)):
                    self.xVel += speed *deltaTime
                    if self.xVel < -maxSpeed :
                        self.xVel+=self.decelSpeed *deltaTime 
                        
                    if self.xVel > maxSpeed: #brings you back to speed if you decelerate too much
                        self.xVel = -maxSpeed 
                         
                elif self.xVel < -maxBoost  and (boostButton or self.homeTo!=(0,0)):
                    self.xVel += speed *deltaTime
                    if self.xVel < -maxBoost :
                        self.xVel+=self.decelSpeed *deltaTime   
                        
                    if self.xVel > -maxBoost: #brings you back to speed if you decelerate too much
                        self.xVel = -maxBoost
                        
                           
            self.xVel = round(self.xVel,2)
            if str(abs(self.xVel))[:3] == "0.1" or str(abs(self.xVel))[:3] == "0.0":
                self.xVel = 0
        else:
            self.xVel = 0


        if abs(self.xVel) > self.terminalVelocityX:
            self.xVel = self.terminalVelocityX*self.getDirNum() *deltaTime

        self.changeX((self.xVel)*deltaTime+sign(self.xVel))
        
    #@profile
    def gravity(self):
        
        level.levelPosy = round(level.levelPosy, 2)
        if level.levelPosy > level.lowestPoint:
            print(level.lowestPoint, level.levelPosy, level.levelVis.get_height())
            self.die()
            pass
        
        if self.yVel > 0:
            self.y+=self.yVel*deltaTime
            level.levelPosy = self.y
            if level.checkCollision(self.charRect):
                self.kTime = defaultKTime
                self.yVel = 0
                self.stomp = False
                self.decelSpeed = 0.2
            
        for i in range(-int(self.yVel)):
            self.y-=deltaTime
            level.levelPosx, level.levelPosy = self.x, self.y
            self.checkCeiling()
            
        if not level.checkCollision(self.charRect):
            self.yVel+=0.5*deltaTime
            if self.yVel > self.terminalVelocityY*deltaTime:
                self.yVel = self.terminalVelocityY*deltaTime
            self.kTime -= 1
            self.wallJumpKTime -= 1
            if self.kTime<0:
                self.kTime=0
                self.decelSpeed = 0.05
        if self.homeTo == (0,0):
            level.levelPosy+=1
            self.touchGround = level.checkCollision(self.charRect)
            level.levelPosy-=1
            while self.touchGround:
                level.levelPosy = self.y+1
                if not level.checkCollision(self.charRect):
                    self.yVel=+1 *deltaTime
                    self.y+=1
                    level.levelPosy = self.y
                    self.touchGround=False
                    self.kTime = 0
                else:
                    self.y-=0.1
                    level.levelPosy = self.y
                    self.touchGround = level.checkCollision(self.charRect)
                    self.kTime = defaultKTime
                    self.wallJumpKTime = 0
                    self.jumpAnimateFrame = 0
                    self.stomp = False
                    self.jumpsLeft = 2


            if semiLevel.checkCollision(self.charRect):
                level.levelPosy-=int(self.yVel)+1
                if not semiLevel.checkCollision(self.charRect):
                    level.levelPosy+=1
                    player.decelSpeed = 0.2
                    self.yVel = 0
                    self.touchGround = True
                    self.stomp = False
                    touchSemi = self.semied
                    self.semied = True
                    while not touchSemi:
                        level.levelPosy+=1
                        touchSemi = semiLevel.checkCollision(self.charRect)
                        self.kTime = defaultKTime
                        self.wallJumpKTime = 0
                        self.jumpAnimateFrame = 0
                        self.jumpsLeft = 2
                else:
                    level.levelPosy+=int(self.yVel)+1
                    if self.semied:
                        self.kTime = defaultKTime
                        self.wallJumpKTime = 0
                        self.jumpAnimateFrame = 0
                    self.semied = False
                level.levelPosy-=1
                self.y = level.levelPosy
            elif self.semied and not inputs.inputEvent("Jump"):
                self.kTime = defaultKTime
                self.wallJumpKTime = 0
                self.jumpAnimateFrame = 0
                self.semied = False
            elif self.semied:
                self.semied = False




        
        global stompHeld
        if not self.climbedLastFrame and self.kTime < 8:
            if inputs.inputEvent("Stomp", False) and not stompHeld and not self.climbedLastFrame:
                
                self.stomp = True
                self.yVel = 20 *deltaTime
                stompHeld = True
                
                self.stompVel = self.xVel + 5*sign(self.xVel)
                
        inputs.inputEvent("UIBACK", False)
                
        




    def checkCeiling(self):
        level.levelPosy = self.y-1
        self.charRect.height = 1
        if level.checkCollision(self.charRect):
            self.yVel=+1
            while level.checkCollision(self.charRect):
                self.y+=1
                level.levelPosy = self.y 
            self.touchGround=False
            self.kTime = 0
            self.charRect.height = 30
            return True
        else:
            self.charRect.height = 30
            return False


    def getDirNum(self):
        if self.isRight:
            return 1
        else:
            return -1
        
#endregion PLAYER MOVEMENT AND PHYSICS

    def update(self):
        
        level.levelPosx, level.levelPosy = self.x, self.y
        
        if self.wallJumpDelay > 0:
            self.wallJumpDelay -= 1

        if self.maxBoost > self.defaultBoost and self.homeTo == (0,0):
            self.maxBoost -= self.decelSpeed

        if self.stomp:
            self.terminalVelocityY = 25
        else:
            self.terminalVelocityY = 17



        if not self.resetFrame: self.gravity()
        
        
        if self.homeTo != (0,0):
            self.homingTo()
            
        self.superBoostCoolDownFull = self.superBoostCoolDown + self.superBoostCoolDownCoins
 

        if (inputs.inputEvent("Dash", False) or self.dashInputBuffer > 0) and (self.superBoostCoolDown <= 0 or self.superBoostCoolDownCoins <= 0):
            self.bounce = False
            self.maxBoost = (gameManager.speed*3)+ self.superBoost
            self.xVel += self.superBoost*self.getDirNum()
            inputs.rumble(0.1, abs(self.xVel/10)+0.3, 100)
            
            audioPlayer.playSound(resources.sounds["player"]["dash"])
            
            particleColour = YELLOW
            
            coolDownToRemove = self.maxBoostCoolDown
            if self.superBoostCoolDownCoins <= 0:
                self.superBoostCoolDownCoins += coolDownToRemove
                coolDownToRemove = 0
                particleColour = ORANGE
            elif self.superBoostCoolDown <= 0:
                self.superBoostCoolDown += coolDownToRemove
                coolDownToRemove = 0
            
            
            self.homeTo = (0,0)
            self.stomp = False
            if self.yVel > -3:
                self.yVel = -3
            
            for i in range(2):
                gameManager.addParticle(Particle(self.x + 10, self.y+15, -self.xVel, random.randint(1, 4), 20, 20, 10, particleColour))
                gameManager.addParticle(Particle(self.x + 10, self.y+15, -self.xVel, -random.randint(1, 4), 20, 20, 10, particleColour))
                
        elif self.superBoostCoolDown>0:
            if self.kTime == 10: self.superBoostCoolDown-=deltaTime
            hud.getElementByTag("boostBar").style.colour = RED
            hud.getElementByTag("boostBar").updateSurface()
            
            self.dashInputBuffer -= 1 if self.dashInputBuffer > 0 else 0
            
            if inputs.inputEvent("Dash", False):
                self.dashInputBuffer = 10
            
        elif self.superBoostCoolDown<=-self.maxBoostCoolDown:
            hud.getElementByTag("boostBar").style.colour = ORANGE
            hud.getElementByTag("boostBar").updateSurface()

        elif self.superBoostCoolDown<=0:
            hud.getElementByTag("boostBar").style.colour = YELLOW
            hud.getElementByTag("boostBar").updateSurface()

        self.resetFrame = False

        
        if inputs.inputEvent("Jump", False):
            inputs.inputEvent("UIACCEPT", False)
            self.jump()
            
        if abs(self.xVel) > self.maxSpeed * 2:
            if self.speedParticleCoolDown <= 0:
                randNum =random.randint(10, 25)
                self.speedParticles.append(Particle(self.x + (-20 if sign(self.xVel) == -1 else 30), self.y + random.randint(0, 30), self.xVel/1.3, 0, randNum, 2, 5, WHITE))
                gameManager.addParticle(self.speedParticles[-1])
                self.speedParticleCoolDown = randNum/(abs(self.xVel)/2)
            else:
                self.speedParticleCoolDown -= deltaTime
        elif len(self.speedParticles) > 0 and abs(self.xVel) <= 0.1:
           self.killSpeedParticles()
                
                
        level.checkEntityCollision(self)
        
        if inputs.inputEvent("Interact", False) and self.kTime == defaultKTime and self.xVel == 0:
            level.checkCollision(self.charRect, True, [37])
            
        self.lockMovement = False
        level.checkCollision(self.charRect, True, [9])
        level.checkCollision(self.charRect, True, [2, 4, 5, 6, 7, 8, 11, 12, 13, 14, 23, 24, 26, 29, 30, 35, 38])
        

    
    def killSpeedParticles(self):
        for particle in self.speedParticles:
            particle.kill()
        
    def levelUp(self):
        self.minCoinCoolDown -= self.maxBoostCoolDown
        hud.getElementByTag("fullBoostBar").updateSize(200 + (100*abs(self.minCoinCoolDown/self.maxBoostCoolDown)), 20)
        
        

    def homingTo(self):
        if self.homeRight:
            if level.levelPosx < self.homeTo[0]:
                self.changeXVel(self.homeSpeed, True)
            if level.levelPosx >= self.homeTo[0]:
                self.xVel = 0
                self.changeX(self.homeTo[0]-level.levelPosx)
                level.updateTiles()
        elif not self.homeRight:
            if level.levelPosx > self.homeTo[0]:
                self.changeXVel(self.homeSpeed, False)
            if level.levelPosx <= self.homeTo[0]:
                self.xVel = 0
                self.changeX(self.homeTo[0]-level.levelPosx)
                level.updateTiles()
                
        if self.homeDown:
            if level.levelPosy < self.homeTo[1]:
                self.yVel += self.homeSpeed
            if level.levelPosy >= self.homeTo[1]:
                self.yVel = (level.levelPosy-self.homeTo[1])*-1
                level.updateTiles()
        elif not self.homeDown:
            if level.levelPosy > self.homeTo[1]:
                self.yVel -= self.homeSpeed
            if level.levelPosy <= self.homeTo[1]:
                self.yVel = self.homeTo[1]-level.levelPosy
                level.updateTiles()
                
    
    def executeJump(self):
        audioPlayer.playSound(resources.sounds["player"]["jump"])
        self.bounce = False
        self.yVel = -self.jumpPower 
        self.kTime=0
        self.jumpsLeft-=1
        self.wallJumpDelay = 20    
                
                
    def jump(self):
        level.levelPosy+=1
        if (self.touchGround or self.kTime>0):
            self.executeJump()
        elif self.wallJumpKTime > 0:
            self.executeWallJump(self.wallJumpKTimeDirection)
        level.levelPosy-=1

    def animate(self):
        
        animateFrame = 0
        animationRotation = 0
        
        
        walkAnimateFrame = int(self.walkAnimateFrame)
        if self.xVel == 0:
            animateFrame = 0
        elif abs(self.xVel) > 0 and self.touchGround or self.kTime>0:
            if walkAnimateFrame in [0, 2]:
                animateFrame = 0
            elif walkAnimateFrame == 1:
                animateFrame = 1
            else:
                animateFrame = 2
                
        if self.kTime != defaultKTime or self.xVel != 0:
            self.idleAnimating = False
            self.idleAnimationTimer = 120
        if not self.idleAnimating:
            if self.kTime == defaultKTime and self.xVel == 0:
                self.idleAnimationTimer -= deltaTime
                if self.idleAnimationTimer <= 0:
                    self.idleAnimationTimer = 0
                    if random.randint(1, 5) == 5:
                        self.idleAnimating = True
                        self.currentIdleAnimation = random.choice(list(self.animations.keys()))
                        self.animations[self.currentIdleAnimation].reset()
            else:
                self.idleAnimating = False
                self.idleAnimationTimer = 120
        else:
            animateFrame = self.animations[self.currentIdleAnimation].getFrame()
            if self.animations[self.currentIdleAnimation].finished:
                self.idleAnimating = False
                self.idleAnimationTimer = 120
        
        if abs(self.xVel) > self.maxSpeed*2 and (self.touchGround or self.kTime>0):
            if walkAnimateFrame in [0, 2]:
                animateFrame = 8
            elif walkAnimateFrame == 1:
                animateFrame = 9
            else:
                animateFrame = 10

        if self.yVel > 2:
            animateFrame = 3

        if int(self.yVel) == 12:
            animateFrame = 4
        elif self.yVel > 12:
            animateFrame = 5
        elif self.yVel < 0 or self.homeTo != (0,0):
            if not self.bounce:
                self.jumpAnimateFrame += 0.25
                if self.jumpAnimateFrame == 8:
                    self.jumpAnimateFrame = 0
                if int(self.jumpAnimateFrame)%2 == 0:
                    animateFrame = 6
                    animationRotation = -90*int(self.jumpAnimateFrame/2)
                    

                else:
                    animateFrame = 7
                    animationRotation = -90*(int((self.jumpAnimateFrame)-1)/2)
                self.hatOffset = (-20 * (1 if self.isRight else -1) if animationRotation < -90 else 0, 20 if animationRotation in [-90, -180] else 0)
                
            else:
                self.jumpAnimateFrame += 0.25
                if self.jumpAnimateFrame >= 4:
                    self.jumpAnimateFrame = 0
                if self.jumpAnimateFrame >= 0:
                    animateFrame = 14
                if self.jumpAnimateFrame >= 1:
                    animateFrame = 15
                if self.jumpAnimateFrame >= 2:
                    animateFrame = 16
                if self.jumpAnimateFrame >= 3:
                    animateFrame = 17
            
                
        if self.climbedLastFrame: 
            self.hatOffset = (0,0)
            animationRotation = 0
            self.climbedLastFrame=False
            if self.climbAnimateFrame >= 2: animateFrame = 13
            elif self.climbAnimateFrame >= 1: animateFrame = 12
            elif self.climbAnimateFrame >= 0: animateFrame = 11


        returnImage = playerImages[animateFrame]
        returnHat = pygame.Surface((0,0))
        if self.hat != "none":
            try:
                returnHat = playerHatImages[animateFrame]
            except IndexError:
                returnHat = playerHatImages[0]
            
        if animationRotation != 0:
            returnImage = pygame.transform.rotate(returnImage, animationRotation)
            if self.hat != "none":
                returnHat = pygame.transform.rotate(returnHat, animationRotation)
            
        if not self.isRight:
            returnImage = pygame.transform.flip(returnImage, True, False)
            if self.hat != "none":
                returnHat = pygame.transform.flip(returnHat, True, False)

        return (returnImage, returnHat)

    def draw(self):
       
        self.blitPosX = self.x - gameManager.camera.x - 5
        self.blitPosY = self.y - gameManager.camera.y - 175
        
        self.hatOffset = (0,0)
        
        if not waiting and not uiPause.show:
            self.currentFrames = self.animate()
            
        if debug > 2:
            pygame.draw.rect(win, RED, (self.blitPosX+5, self.blitPosY+1, 20, 30))
        
        # Blit the animated character onto the screen
        win.blit(self.currentFrames[0], (self.blitPosX, self.blitPosY+1))
    
        if self.hat != "none":
            win.blit(self.currentFrames[1], (self.blitPosX - (0 if self.isRight else 20) + self.hatOffset[0], self.blitPosY-19 + self.hatOffset[1]))


        for y, powerUp in enumerate(self.powerUps):
            powerUp.draw(y)

        # if abs(self.xVel) >= self.maxBoost-1 and (self.touchGround or self.kTime>0):
        #     if not self.isRight:
        #         win.blit(pygame.transform.flip(random.choice(boostImages), True, False), (self.charRect.x-5, self.charRect.y))
        #     else:
        #         win.blit(random.choice(boostImages), (self.charRect.x-5, self.charRect.y))


class LevelChunk:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tiles = []
        self.entities = []
        self.trimmedTiles = []
        self.draw = False
        self.camTiles = []
        
    def start(self):
        for tile in self.tiles:
            if type(tile) in [StopLessThanX, StopLessThanY, StopMoreThanX, StopMoreThanY]:
                self.camTiles.append(tile)
    
    def alterCam(self):
        for tile in self.camTiles:
            if tile.singleUpdate(deltaTime): break # breaks the loop if a cam change happens

    def checkCollision(self, rectToCheck, tileToCheck=[0, 10, 15, 16, 17, 18], useTrim = True):
        global collisionTiles
        collided = False
        if useTrim:
            for tile in self.trimmedTiles:  
                collisionTiles += 1  
                if tile.tileID in tileToCheck:
                    tile.updateRect()
                    if tile.checkCollision(rectToCheck):
                        collided = True
        else:#475, 300
            for tile in self.tiles:  
                if tile.tileID in tileToCheck:
                    if tile.rect.x > rectToCheck.x-75 and tile.rect.x < rectToCheck.x +75 and tile.rect.y > rectToCheck.y-100 and tile.rect.y < rectToCheck.y+100: 
                        tile.updateRect()
                        if tile.checkCollision(rectToCheck):
                            collided = True
            
        return collided
    def checkEntityCollision(self, obj):
        for entity in self.entities:
            entity.checkCollision(obj)
    def trimTiles(self):
        self.trimmedTiles = []
        for tile in self.tiles:
            if tile.rect.x+tile.rect.w > 400 and tile.rect.x < 550 and tile.rect.y+tile.rect.w > 200 and tile.rect.y < 400: 
                self.trimmedTiles.append(tile)
    def update(self):
        for tile in self.tiles:
            tile.update()
    def drawEntities(self):
        for entity in self.entities:
            entity.draw(win, debug > 2)
    def singleUpdate(self):
        for tile in self.tiles:
            tile.singleUpdate(deltaTime)
    def entityUpdate(self):
        for entity in self.entities:
            entity.update()
    def posToString(self) -> str:
            return f"{self.x}-{self.y}"
    
    def reset(self):
        endLoop = len(self.entities)
        i=0
        while i!=endLoop:
            if self.entities[i].reset(): # returns true if the entity still exists after reload
                i+=1
            else:
                endLoop-=1
        
                        

class Level:
    def __init__(self):
        self.levelPosx = 0
        self.levelPosy = 0
        self.camX =0
        self.camY =0
        self.lowestPoint = 0
        self.highestPoint = 0
        self.worldXLast, self.worldYLast = -1, -1
        self.levelVis = pygame.Surface((0,0), pygame.SRCALPHA)
        self.levelBG = pygame.Surface((0,0), pygame.SRCALPHA)
        self.levelInteract = pygame.Surface((0,0), pygame.SRCALPHA)
        
        
        self.bg = pygame.Surface((0,0), pygame.SRCALPHA)
        self.paraLayer1 = pygame.Surface((w*2,h), pygame.SRCALPHA)
        self.paraLayer2 = pygame.Surface((w*2,h), pygame.SRCALPHA)
        
        self.quickDraw = keys[pygame.K_SPACE]
        self.offset = 1540
        self.switch = False

        self.levels=[]
        
        self.levelInfo = {}
        
        self.chunks = {}
        self.activeChunks = []
        self.entityChunks = []
        
        self.lvlxlast = 0
        self.lvlylast = 0
        
        self.yOffSet = 0
        
        self.tileHightOffset = 0

        self.loadBG(s.settings["bgType"])
        
        self.toggleBlockState = True
        
        self.objects = {}
        
        self.baseLevelInfo = parseJsonFile(f"levels/CreateNewLevel/sampleInfo.json")
    def lvlSelectChangeLevel(self):
        gameManager.togglePause()
        gameManager.nextLevel()
        
    def moveLevel(self):
        global worldX, worldY
        # worldY+=lvl
        # worldX+=world
        
        gameManager.timerOn = False
        
        
        rank = "e"
        
        if gameManager.timer/60 < self.levelInfo["ranks"]["s"]:
            rank = "s"
            if not self.levelInfo["hats"]["sRank"] in hatManager.hats:
                hatManager.unlockHat(self.levelInfo["hats"]["sRank"])
        elif gameManager.timer/60 < self.levelInfo["ranks"]["a"]:
            rank = "a"
        elif gameManager.timer/60 < self.levelInfo["ranks"]["b"]:
            rank = "b"
        elif gameManager.timer/60 < self.levelInfo["ranks"]["c"]:
            rank = "c"
        elif gameManager.timer/60 < self.levelInfo["ranks"]["d"]:
            rank = "d"
        
        uiResults.show = True
        hud.show = False
        
        uiResults.getElementByTag("rank").changeImages([resources.uiAnimations["rankings"][rank]])
        
        uiResults.getElementByTag("s").updateText(f"S RANK: {gameManager.intToTime(self.levelInfo['ranks']['s'], False)[:-3]}")
        uiResults.getElementByTag("a").updateText(f"A RANK: {gameManager.intToTime(self.levelInfo['ranks']['a'], False)[:-3]}")
        uiResults.getElementByTag("b").updateText(f"B RANK: {gameManager.intToTime(self.levelInfo['ranks']['b'], False)[:-3]}")
        uiResults.getElementByTag("c").updateText(f"C RANK: {gameManager.intToTime(self.levelInfo['ranks']['c'], False)[:-3]}")
        uiResults.getElementByTag("d").updateText(f"D RANK: {gameManager.intToTime(self.levelInfo['ranks']['d'], False)[:-3]}")
        
        player.xVel = 0
        player.yVel = 0
        
        uiResults.getElementByTag("timer").updateText(f"Final Time: {gameManager.intToTime(gameManager.timer // 60)}")
        

    def updateTiles(self):
        if inputs.inputEvent("toggleBlocks", False):
            self.toggleBlockState =  not self.toggleBlockState
        for chunk in self.activeChunks:
            chunk.update()
    def singleUpdateTiles(self):
        for chunk in self.entityChunks:
            chunk.singleUpdate()
        for chunk in self.entityChunks:
            chunk.entityUpdate()
    def updateCameraChanges(self):
        for chunk in self.entityChunks:
            if len(chunk.camTiles) > 0:
                chunk.alterCam()
    
#region LEVEL COLLISION
    def checkCollision(self, rectToCheck, useTrim=True, tileToCheck=[0, 10, 15, 16, 17, 18, 27, 28, 36]):
        global collisionTiles
        collided = False
        collisionTiles = 0
        
        for chunk in self.activeChunks:
            if chunk.checkCollision(rectToCheck, tileToCheck, useTrim): collided = True
            
            # if collided:
            #     return collided
        
        return collided
        
    def checkEntityCollision(self, obj):
        collided = False
        
        for chunk in self.activeChunks:
            collided = chunk.checkEntityCollision(obj)
            
            if collided:
                return collided
        
        return collided
    
#endregion LEVEL COLLISION

#region LOADING LEVELS
    def loadBG(self, bgName):
        self.bg = pygame.image.load(f"levelAssets/backgrounds/{bgName}/bg.png").convert()
        
        paraLayer1 = pygame.image.load(f"levelAssets/backgrounds/{bgName}/layer1.png").convert_alpha()
        paraLayer2 = pygame.image.load(f"levelAssets/backgrounds/{bgName}/layer2.png").convert_alpha()
        
        
        self.paraLayer1 = Background(paraLayer1, 4)
        # self.paraLayer1.blit(paraLayer1, (0,0))
        # self.paraLayer1.blit(paraLayer1, (w,0))
        
        self.paraLayer2 = Background(paraLayer2, 2)
        # self.paraLayer2.blit(paraLayer2, (0,0))
        # self.paraLayer2.blit(paraLayer2, (w,0))


    def addTile(self, newTile):
        self.levels.append(newTile)
                                
              
        
        #set vars needed for tiles
        newTile.index = len(self.levels)
        newTile.level = self
        newTile.player = player
        newTile.gameManager = gameManager
        newTile.win = win
        
    
    #@profile
    def changeLevel(self, resetPlayerPos=True, reloadLevel=False):
        self.loading = True
        self.first = True
        groundTiles = ["0"]
        pygame.mixer.Channel(7).fadeout(500)
        self.toggleBlockState = True
        
        win.fill(BLACK)
        win.blit(loadingFactFont.render(random.choice(facts), True, WHITE), (0,600))
        # win.blit(loadingFactFont.render(facts[-1], True, WHITE), (0,600))
        
        win.blit(bigFont.render("Reading level data...", True, WHITE), (0,90))
        
        win.blit(pygame.transform.scale(playerImages[0], (90, 90)), (1190, 630))

        
        window.blit(win, (0,0))
        pygame.display.flip()
        
        
        self.chunks = {}
        self.activeChunks = []
        
        #self.quickDraw = True
        self.worldXLast, self.worldYLast = worldX, worldY
        self.levels = []
        
        
        self.levelInfo = parseJsonFileWithBase(f"levels/levelInfo/{worldX}-{worldY}.json", self.baseLevelInfo)
        
        levelJson = parseJsonFile(f"levels/levels/{worldX}-{worldY}.json")
        
        self.loading = False
        
        self.objects = {}
        
        resliceImages(self.levelInfo["tileMapType"])
        
        decals = []
        loadedDecalImages = {}
        
        
        #loads the background into memory
        self.loadBG(self.levelInfo['bgType'])        
        # saves the background to the settings as the last used background
        s.settings["bgType"] = self.levelInfo["bgType"]
        s.updateSettings()
        
        self.lowestPoint = 0
        self.highestPoint = float('inf')
        
        
        levelMap = {}
        
        chunksTemp = []
        
        self.indexOffset = 0
        
        largestX = 0
        for layer in levelJson["layers"]:
            if layer["type"] == "tilelayer":
                for chunk in layer["chunks"]:
                    chunkX = chunk["x"]
                    chunkY = chunk["y"]
                    if(not f"{chunkX}-{chunkY}" in self.chunks):
                        chunksTemp.append(LevelChunk(int(chunkX), int(chunkY)))
                    for y in range(16):
                        for x in range(16):
                            if chunk["data"][(y*16) + x] != 0:
                                newTile = createTile((chunkX + x)*tileSize, (chunkY + y)*tileSize, int(chunk["data"][(y*16) + x])-1, tileSize)
                                
                                self.addTile(newTile)                  
                                if (chunkX + x)  > largestX:
                                    largestX = (chunkX + x)
                                
                                if layer["name"] == "Main":
                                    if (chunkY + y)*tileSize < self.highestPoint:
                                        self.highestPoint = (chunkY + y)*tileSize
                                    
                                    elif (chunkY+y)*tileSize > self.lowestPoint:
                                        self.lowestPoint = (chunkY+y)*tileSize
                                
                                
            elif layer["type"] == "objectgroup":
                for obj in layer["objects"]:
                    if obj["type"].lower() == "tile":
                        self.objects[obj["id"]] = Object(obj["x"], obj["y"], obj["name"], obj["type"], self, obj, obj["gid"])
                    elif obj["type"].lower() == "decal":
                        imgString = obj["properties"][0]["value"][6:]
                        if not imgString in loadedDecalImages:
                            loadedDecalImages[imgString] = pygame.image.load(imgString).convert_alpha()
                        decals.append(Decal(obj["x"], obj["y"], loadedDecalImages[imgString]))
                    else:
                        self.objects[obj["id"]] = Object(obj["x"], obj["y"], obj["name"], obj["type"], self, obj)
                        
                            
        
        
        self.tileHightOffset = -self.highestPoint
            
        for chunk in chunksTemp:
            chunk.y+=int(self.tileHightOffset)
            self.chunks[chunk.posToString()] = chunk
            
        del chunksTemp
            
        
        for tile in self.levels:
            tile.y += int(self.tileHightOffset)
            tilex = int((tile.x/tileSize)/16)*16
            tiley = int((tile.y/tileSize)/16)*16
            if not f"{int(tilex)}-{int(tiley)}" in self.chunks:
                self.chunks[f"{int(tilex)}-{int(tiley)}"] = LevelChunk(tilex, tiley)
            self.chunks[f"{int(tilex)}-{int(tiley)}"].tiles.append(tile)
            self.chunks[f"{int(tilex)}-{int(tiley)}"].tiles[-1].chunk = self.chunks[f"{int(tilex)}-{int(tiley)}"]
            
        
        for tile in self.levels: # adds tiles to the level map with it's type as they key, done after offsetting so values are not changed
            idStr = str(tile.tileID)
            if not idStr in levelMap:
                levelMap[idStr] = {}
            
            levelMap[idStr][f"{tile.x}, {tile.y}"] = True
        
        self.lowestPoint += self.tileHightOffset+tileSize
        
        self.levelVis = pygame.Surface((largestX*tileSize, self.lowestPoint), pygame.SRCALPHA)
        self.levelVis.fill((0,0,0,0))
        
        self.levelBG = pygame.Surface((largestX*tileSize, self.lowestPoint), pygame.SRCALPHA)
        self.levelBG.fill((0,0,0,0))
        
        self.levelInteract = pygame.Surface((largestX*tileSize, self.lowestPoint), pygame.SRCALPHA)
        self.levelInteract.fill((0,0,0,0))
        
        self.levelToggleON = pygame.Surface((largestX*tileSize, self.lowestPoint), pygame.SRCALPHA)
        self.levelToggleON.fill((0,0,0,0))
        self.levelToggleOFF = pygame.Surface((largestX*tileSize, self.lowestPoint), pygame.SRCALPHA)
        self.levelToggleOFF.fill((0,0,0,0))
        
        self.lowestPoint+=174
        
        
        gameManager.camXLim = self.levelVis.get_width() - w
        gameManager.camYLim = self.levelVis.get_height() - h
        
        gameManager.camXMin = 0
        gameManager.camYMin = 0
        
        gameManager.camera.setLevelEdgeMaxes(gameManager.camXLim, gameManager.camYLim)
        gameManager.camera.setMins(0, 0)
    

        
        animateLoadFrame = 0
        tilesLoaded = 0
        if not self.quickDraw:
            loadingText = ""
            for tile in self.levels:
                if tile.tileID == 3 and resetPlayerPos:
                    spawnPos = self.getSpawn()
                    gameManager.ogSpawn = spawnPos
                    self.levelPosx, self.levelPosy = spawnPos[0], spawnPos[1]
                    player.x, player.y = spawnPos[0], spawnPos[1]
                    player.lastSpawn = (self.levelPosx, self.levelPosy)
                if tile.tileID != "-1":
                    if loadingText !=  f"{str(int((tilesLoaded/len(self.levels))*100))}%":
                        pygame.draw.rect(win, BLACK, pygame.Rect(0, 0, w, h/2))
                        win.blit(bigFont.render(f"Loading Level: {str(int((tilesLoaded/len(self.levels))*100))}%", True, WHITE), (0,90))
                        animateLoadFrame += 1
                        if animateLoadFrame > 15:
                            animateLoadFrame = 0
                        pygame.draw.rect(win, BLACK, (1190, 630, 90, 90))
                        win.blit(pygame.transform.scale(playerImages[int(animateLoadFrame/5) + 14], (90, 90)), (1190, 630))
                        window.blit(win, (0,0))
                        pygame.display.update()
                        loadingText = f"{str(int((tilesLoaded/len(self.levels))*100))}%"
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quitGame()
                    
                    #tile.image = slope
                    
                    if tile.tileID == 0:
                        self.getTileImage(tile, levelMap, "0", tilesLoaded, tileImages.groundImages)
                    elif tile.tileID == 1:
                        self.getTileImage(tile, levelMap, "1", tilesLoaded, tileImages.bridgeImages, ["0", "1", "15", "16", "17"])
                    elif tile.tileID == 2:
                        self.getTileImage(tile, levelMap, "2", tilesLoaded, tileImages.spikeImages, ["0", "2", "15", "16", "17"])
                    elif tile.tileID == 4:
                        tile.image = tileImages.objectImages[1]
                    elif tile.tileID == 5:
                        tile.image = tileImages.objectImages[3]
                    elif tile.tileID == 6:
                        tile.image = tileImages.objectImages[0]
                    elif tile.tileID == 7:
                        tile.image = tileImages.objectImages[4]
                    elif tile.tileID == 8:
                        tile.image = tileImages.objectImages[2]
                    elif tile.tileID == 10:
                        tile.image = tileImages.objectImages[5]
                    elif tile.tileID == 14:
                        tile.image = tileImages.objectImages[6]
                    elif tile.tileID == 15:
                        self.getTileImage(tile, levelMap, "15", tilesLoaded, tileImages.groundBImages)
                    elif tile.tileID == 16:
                        self.getTileImage(tile, levelMap, "16", tilesLoaded, tileImages.groundCImages, ["16", "17"])
                    elif tile.tileID == 17:
                        self.getTileImage(tile, levelMap, "17", tilesLoaded, tileImages.groundDImages, ["16", "17"])
                        
                    elif tile.tileID == 18:
                        self.getTileImage(tile, levelMap, "18", tilesLoaded, tileImages.backGroundAImages, ["0", "15", "16", "17", "18", "19"])
                    elif tile.tileID == 19:
                        self.getTileImage(tile, levelMap, "19", tilesLoaded, tileImages.backGroundBImages, ["0", "15", "16", "17", "18", "19"])
                    elif tile.tileID == 20:
                        self.getTileImage(tile, levelMap, "20", tilesLoaded, tileImages.backGroundCImages, ["0", "15", "16", "17", "20", "21"])
                    elif tile.tileID == 21:
                        self.getTileImage(tile, levelMap, "21", tilesLoaded, tileImages.backGroundDImages, ["0", "15", "16", "17", "20", "21"])
                    elif tile.tileID == 22:
                        self.getTileImage(tile, levelMap, "22", tilesLoaded, tileImages.movingPlatformImages, ["22"])
                    elif tile.tileID == 23:
                        tile.image = tileImages.objectImages[11]
                    elif tile.tileID == 27:
                        tile.image = tileImages.objectImages[12]
                    elif tile.tileID == 28:
                        tile.image = tileImages.objectImages[13]
                    elif tile.tileID == 29:
                        tile.image = tileImages.objectImages[14]
                    elif tile.tileID == 30:
                        tile.image = tileImages.objectImages[15]
                    elif tile.tileID == 35:
                        tile.image = tileImages.objectImages[18]
                    tilesLoaded+=1
                
        else:
            for tile in self.levels:
                pass
            print("pretty sure this never runs")
                    

        pygame.draw.rect(win, BLACK, pygame.Rect(0, 0, w, h/2))
        win.blit(bigFont.render("Almost Done...", True, WHITE), (0,90))
        pygame.draw.rect(win, BLACK, (1190, 630, 90, 90))
        win.blit(pygame.transform.scale(playerImages[0], (90, 90)), (1190, 630))
        window.blit(win, (0,0))
        pygame.display.update()
                
        for tile in self.levels:
            tile.start()
            tile.levelDraw()
        for chunk in self.chunks.values():
            chunk.start()
        
        for decal in decals:
            decal.draw(self.levelVis, self.tileHightOffset)
        
        deletedTiles = 100
        # Collect tiles to be deleted in one pass and update indexes if needed
        deleted_tiles_list = []
        new_levels = []
        self.levels[:] = [tile for tile in self.levels if not tile.checkDelete()]

        # for tile in self.levels:
        #     tile.index -= self.indexOffset
        #     tile.checkDelete()
            
        self.trimLevel(True)
        audioPlayer.playMusic(MusicSource(f"{self.levelInfo['music']}"), s.settings["musicVolume"]/100)
        
        player.lastSpawn = gameManager.ogSpawn
        player.reset()
        
        global titleLerpStall, titleLerpStage
        titleLerpStall = 180
        titleLerpStage = 0
        
        uiLevelTitle.show = True
        uiLevelTitle.getElementByTag("lvlName").resetPosition()
        uiLevelTitle.getElementByTag("lvlName").startLerp((100, 100), 0.1)
        uiLevelTitle.getElementByTag("lvlName").updateText(self.levelInfo["name"])
        
        uiLevelTitle.getElementByTag("bg").resetPosition()
        uiLevelTitle.getElementByTag("bg").startLerp((0, 125), 0.1)
        
        
        gameManager.timerOn = True
        
        gameManager.finalUpdate()
        
        self.loading = False
        
    def getTileImage(self, tile, levelMap, typeNum:str, tilesLoaded, tilesToBeUsed, groundTiles=["0", "15"]):
        above, below, left, right = False, False, False, False
        # Define a dictionary to map neighbor patterns to tile images
        neighbor_image_map = {
            (False, True, False, True): 0,
            (False, True, True, True): 1,
            (False, True, True, False): 2,
            (False, True, False, False): 4,
            (False, False, False, False): 6,
            (True, True, False, True): 9,
            (True, True, True, True): 10,
            (True, True, True, False): 11,
            (True, True, False, False): 13,
            (True, False, False, True): 18,
            (True, False, True, True): 19,
            (True, False, True, False): 20,
            (True, False, False, False): 22,
            (False, False, False, True): 24,
            (False, False, True, True): 25,
            (False, False, True, False): 26,
        }

        wasFirst = self.first
        
        for t in groundTiles:
            if t in levelMap:
                    
                if f"{tile.x}, {tile.y-tileSize}" in levelMap[t]:
                    above = True
                if f"{tile.x}, {tile.y+tileSize}" in levelMap[t]:
                        below = True
                if f"{tile.x-tileSize}, {tile.y}" in levelMap[t]:
                    left = True
                if f"{tile.x+tileSize}, {tile.y}" in levelMap[t]:
                    right = True
            
        # Get the corresponding image based on neighbor pattern
        neighbors = (above, below, left, right)
        self.levels[tilesLoaded].image = tilesToBeUsed[neighbor_image_map.get(neighbors, 6)]
        tile.image = tilesToBeUsed[neighbor_image_map.get(neighbors, 6)].convert_alpha()
        
        newImage = pygame.Surface((tileSize,tileSize), pygame.SRCALPHA)
        newImage.blit(tile.image, (0,0))

        topRight, topLeft = False, False
        bottomRight, bottomLeft = False, False

        for t in groundTiles: 
            if t in levelMap:
                if f"{tile.x+tileSize}, {tile.y-tileSize}" in levelMap[t]: #right up
                    topRight = True
                if f"{tile.x-tileSize}, {tile.y-tileSize}" in levelMap[t]: #left up
                    topLeft = True
                    
                    
                if f"{tile.x+tileSize}, {tile.y+tileSize}" in levelMap[t]: #right down
                    bottomRight = True
                if f"{tile.x-tileSize}, {tile.y+tileSize}" in levelMap[t]: #left down
                    bottomLeft = True
                    
        
        #14 for the other
        if not topRight and above and right:
            newImage.blit(tilesToBeUsed[5], (0,0))
        if not topLeft and above and left:
            newImage.blit(tilesToBeUsed[7], (0,0))
        if not bottomRight and below and right:
            newImage.blit(tilesToBeUsed[14], (0,0))
        if not bottomLeft and below and left:
            newImage.blit(tilesToBeUsed[16], (0,0))
        
        tile.image = newImage
        if neighbor_image_map.get(neighbors, 6) == 10:
            tile.toBeDeleted = True

    def reloadTiles(self):
        self.toggleBlockState = True
        for tile in self.levels:
            tile.reload()
        for chunkKey in self.chunks:
            self.chunks[chunkKey].reset()
            
    def getSpawn(self):
        for tilesLoaded, tile in enumerate(self.levels):
            if tile.tileID == 3:
                return (self.levels[tilesLoaded].x, self.levels[tilesLoaded].y+160)
        return (0,0)
    
#endregion LOADING LEVELS

    def trimLevel(self, forceLoad=False):
        
        
        lvlx = int((self.levelPosx / tileSize) / 16) * 16
        lvly = int((self.levelPosy / tileSize) / 16) * 16

        # Define offsets for nearby chunks
        offsets = [(0, 0), (16, 0), (-16, 0), (0, 16), (16, 16), (-16, 16), (0, -16), (16, -16), (-16, -16)]
        entityOffsets = [(-16, -32), (0, -32), (16, -32), (-16, 32), (0, 32), (16, 32), (32, -16), (32, 0), (32, 16), (-32, -16), (-32, 0), (-32, 16), (32, 32), (-32, 32), (-32, -32), (32, -32)]

        self.activeChunks = []
        self.entityChunks = []
        self.lvlxlast = lvlx
        self.lvlylast = lvly

        # Check nearby chunks using offsets, saves tile active chunks and nearby entity chunks
        for offset in offsets:
            x_offset, y_offset = offset
            chunk_key = f"{lvlx + x_offset}-{lvly + y_offset}"
            if chunk_key in self.chunks:
                self.activeChunks.append(self.chunks[chunk_key])
                self.entityChunks.append(self.chunks[chunk_key])
        # does the same but only for entity chunks
        for offset in entityOffsets:
            x_offset, y_offset = offset
            chunk_key = f"{lvlx + x_offset}-{lvly + y_offset}"
            if chunk_key in self.chunks:
                self.entityChunks.append(self.chunks[chunk_key])
            

        # Process tiles in active chunks
        self.onScreenLevel = []
        for chunk in self.entityChunks:
            chunk.trimTiles()
            for tile in chunk.tiles:
                if 0 < tile.rect.x < 1280 and 0 < tile.rect.y < 720:
                    self.onScreenLevel.append(tile)
                    
    
#region rendering 
    def drawEntities(self):
        for chunk in self.entityChunks:
            if len(chunk.entities) > 0:
                chunk.drawEntities()
                
    def drawBG(self, useCrop = True):
        bgDetail = s.settings["backgroundDetail"]
        
        # Blit background
        if bgDetail > 0:
            win.blit(self.bg, (0, 0))

        # Calculate sub-surface position
        if useCrop:
            self.camX = max(0, min(self.levelVis.get_width() - w, self.levelPosx - 635))
            self.camY = max(0, min(self.levelVis.get_height() - h, self.levelPosy - 520)) # I'm gonna keep it a buck fifty, I have no idea why 520 works here
        else:
            self.camX = self.levelPosx
            self.camY = self.levelPosy
        
        if bgDetail == 2:
            # call draw functions of background objects
            self.paraLayer1.draw(win, gameManager.camera.x)
            self.paraLayer2.draw(win, gameManager.camera.x)
        

    def draw(self):
        
        self.drawBG()

        # Create and blit sub-surfaces
        subsurfaceBG = self.levelBG.subsurface((gameManager.camera.x, gameManager.camera.y, w, h))
        subsurfaceInter = self.levelInteract.subsurface((gameManager.camera.x, gameManager.camera.y, w, h))
        if self.toggleBlockState:
            subsurfaceToggle = self.levelToggleON.subsurface((gameManager.camera.x, gameManager.camera.y, w, h))
        else:
            subsurfaceToggle = self.levelToggleOFF.subsurface((gameManager.camera.x, gameManager.camera.y, w, h))
        subsurface = self.levelVis.subsurface((gameManager.camera.x, gameManager.camera.y, w, h))

        win.blit(subsurfaceBG, (0, 0))
        win.blit(subsurfaceInter, (0, 0))
        win.blit(subsurfaceToggle, (0, 0))
        win.blit(subsurface, (0, 0))
        
        
        self.drawEntities()
        
        
        
        

        if debug > 2:
            pygame.draw.rect(win, RED, player.charRect)
            for chunk in self.activeChunks:
                for tile in chunk.trimmedTiles:
                    pygame.draw.rect(win, WHITE, tile.rect)
        
        # old level draw code
        # win.blit(self.levelVis, (-self.levelPosx+475,-self.levelPosy+475))
        
        
        
        # silly :3
        # self.levelVis.blit(logo[0], (self.levelPosx, self.levelPosy))
        
        
        #win.blit(pygame.Surface.subsurface(self.levelVis, (self.camX, self.levelVis.get_height()-h), (w, h)), (0,0))
        
        # full level view
        #win.blit(pygame.transform.scale(self.levelVis, (w,h)), (0,0))
       
#endregion Rendering    

class semiLevel:
    def __init__(self):
        pass
    def checkCollision(self, rectToCheck, tilesToCheck=[1, 22]):
        feetRect = pygame.Rect(475, player.charRect.y+29, 20, 1)
        collided = False
        if player.yVel >= 0:
            collided = level.checkCollision(rectToCheck, True, tilesToCheck)
        return collided and not inputs.inputEvent("Stomp")
    def draw(self):
        #win.blit(self.image, (-level.levelPosx+475,0))
        pass




class DebugLogText:
    def __init__(self, text, showTime = 60, icon="good"):
        self.text = text
        self.showTime = showTime
        self.bg = pygame.Surface((w, 26), pygame.SRCALPHA)
        self.bg.fill((255,255,255,200))
        
        self.icon = pygame.image.load(f"ui/debug/icons/{icon}.png").convert_alpha()
    
    def draw(self, y):
        win.blit(self.bg, (0, (y*26)))
        win.blit(self.icon, (0, (y*26)))
        win.blit(debugLogFont.render(self.text, True, BLACK), (32, ((y*26)+3)))
        self.showTime-=1
        if self.showTime<=0:
            debugLog.remove(self)

from UI import *

class AudioPlayer:
    def __init__(self) -> None:
        self.music = MusicSource("hub/city/discovered.wav")
    def playSound(self, soundSrc, volume=2, channel=0):
        sound = soundSrc.sound
        sound.set_volume(volume if volume != 2 else s.settings["sfxVolume"]/100)
        if channel != 0 or channel > 6:
            pygame.mixer.Channel(channel).play(sound)
        else:
            sound.play()
    def playMusic(self, musicSrc, volume=2):
        pygame.mixer.Channel(7).stop()
        self.music = musicSrc.sound
        self.music.set_volume(volume if volume != 2 else s.settings["musicVolume"]/100)
        pygame.mixer.Channel(7).play(self.music, -1)
             
class MusicSource:
    def __init__(self, soundPath:str) -> None:
        self.sound = pygame.mixer.Sound("sound/music/" + soundPath)

audioPlayer = AudioPlayer()
audioPlayer.playMusic(MusicSource(f"title.wav"), s.settings["musicVolume"]/100)


jump = AudioSource("jump.mp3")
music = AudioSource("music/music.mp3")

  
def redrawScreen():
    global win
    if s.settings["backgroundDetail"] == 0: win = pygame.Surface((w,h))
        
    if gameManager.inGame:
        level.draw()
        
        #spikes.draw() 

        
        player.draw()
    
    else:
        gameManager.camera.setMaxes(gameManager.camera.x + 1, 0)
        gameManager.camera.x+=1
        level.drawBG(False)

    if(debug > 0):
        debugUi.show = True
        debugUi.getElementByTag("FPSText").updateText("FPS: " + str(int(clock.get_fps())))
        if(debug > 1):
            fullDebugUi.show = True
            fullDebugUi.getElementByTag("x").updateText("X: " + str(level.levelPosx))
            fullDebugUi.getElementByTag("y").updateText("Y: " + str(level.levelPosy))
            fullDebugUi.getElementByTag("ctiles").updateText("Collision Tiles: " + str(collisionTiles))
            fullDebugUi.getElementByTag("stomp").updateText("Stomp: " + str(player.stomp))
            fullDebugUi.getElementByTag("dtime").updateText("DeltaTime: " + str(deltaTime))
            fullDebugUi.getElementByTag("tframes").updateText("Target Frames: " + str(targetFrames))
            fullDebugUi.getElementByTag("tiles").updateText("Tiles: " + str(len(level.levels)))
            
            fullDebugUi.update()
            
    else:
        debugUi.show = False
        fullDebugUi.show = False
        
    
    gameManager.drawParticles(win)

    hud.getElementByTag("boostBar").updateSize(getIntPercentage(player.maxBoostCoolDown-player.superBoostCoolDown, player.maxBoostCoolDown), 20)
    hud.getElementByTag("boostBarCoins").updateSize(getIntPercentage(player.maxBoostCoolDown-player.superBoostCoolDownCoins, player.maxBoostCoolDown), 20)
    hud.draw(win)
    uiPause.draw(win)
    uiPauseButtons.draw(win)
    uiMainMenu.draw(win)
    uiMainMenuQuit.draw(win)
    uiLevelTitle.draw(win)
    uiResults.draw(win)
    uiControls.draw(win)
    uiControlsPC.draw(win)
    uiControlsXbox.draw(win)
    uiHat.draw(win)
    if gameManager.settingsMenu:
        uiSettings.draw(win)
    
    fullDebugUi.draw(win)
    
    debugUi.draw(win)
    
    for y, log in enumerate(debugLog):
        log.draw(y)
        
    #win.blit(pygame.image.load("ui/UI SAMPLES/hud02.png").convert_alpha())
    
    window.blit(win, (0,0))
    
    pygame.display.update()
    

gameManager = GameManager()
player = Player()
gameManager.player = player
keys = pygame.key.get_pressed()
level = Level()
player.reset()
player.hat = s.settings["hat"]
playerImages = resources.reloadPlayerImages(player.hat)
playerHatImages = playerImages[-1]
semiLevel = semiLevel()

debugLog = []

# testEntity = Entity(12419, 1544, 20, 20, playerImages[0])
# testEntity.level = level

spaceHeld = False
stompHeld = False
pauseHeld = False

class InputSystem:
    def __init__(self) -> None:
        self.inputDict = {}
        self.controllerDict = {}
        self.axisDict = {}
        self.hatDict = {}
        self.posx = 0
        self.posy = 0
        self.worldX = 0
        self.worldY = 0
        self.clicked = [False, False, False]
        self.clickDown = [False, False, False]
        self.scrolly = 0
        
        self.heldEvents = []
        
        self.controlType = -1 # -1=unknown 0=key 1=controller
        self.lastControlType = 0 # does not reset upon new frame
        
        self.careForMouse = not joystick.get_init()
        self.controllerWasConnected = joystick.get_init()
        self.controllerReconnectAttemptTimer = 20
        self.controllerReconnectAttempts = 9
        
        self.lastPosx = self.lastPosy = 0
    def setKey(self, keyEnum, inputName:str):
        if inputName in self.inputDict:
            self.inputDict[inputName].append(keyEnum)
        else:
            self.inputDict[inputName] = [keyEnum]
    def setButton(self, buttonNum, inputName:str):
        if inputName in self.controllerDict:
            self.controllerDict[inputName].append(buttonNum)
        else:
            self.controllerDict[inputName] = [buttonNum]
    def setAxis(self, axis, axisRange, inputName):
        if inputName in self.axisDict:
            self.axisDict[inputName].append([axis, axisRange])
        else:
            self.axisDict[inputName] = [[axis, axisRange]]
    def setHat(self, axis, direction, inputName):
        if inputName in self.hatDict:
            self.hatDict[inputName].append([axis, direction])
        else:
            self.hatDict[inputName] = [[axis, direction]]
    def inputEvent(self, inputName:str, canHold=True) -> bool:
        inputted = False
        careForHold = (not inputName in self.heldEvents or canHold)
        if self.controlType == -1 or self.controlType == 0:
            if inputName in self.inputDict and careForHold:
                for keyEnum in self.inputDict[inputName]:
                    if keys[keyEnum]:
                        inputted = True
                        self.controlType = 0
                        self.careForMouse = False
                 
        if self.controlType == -1 or self.controlType == 1:   
            if joystick.get_init():
                if not inputted and inputName in self.controllerDict and careForHold:
                    for button in self.controllerDict[inputName]:
                        if button < joystick.get_numbuttons():
                            if joystick.get_button(button):
                                inputted = True
                                self.controlType = 1
                                self.careForMouse = False
                if not inputted and inputName in self.axisDict and careForHold:
                    for axis in self.axisDict[inputName]:
                        if axis[0] < joystick.get_numaxes():
                            if joystick.get_axis(axis[0]) > axis[1][0] and joystick.get_axis(axis[0]) < axis[1][1]:
                                inputted = True
                                self.controlType = 1
                                self.careForMouse = False
                if not inputted and inputName in self.hatDict and careForHold:
                    for hat in self.hatDict[inputName]:
                        if joystick.get_numhats() > 0:
                            if joystick.get_hat(0)[hat[0]] == hat[1]:
                                inputted = True
                                self.controlType = 1
                                self.careForMouse = False
                        
        if inputted and not canHold:
            self.heldEvents.append(inputName)
        return inputted
    
    def update(self):
        self.resetHeldInputs()
        if self.lastControlType!=-1: self.lastControlType = self.controlType
        self.controlType = -1
        
        self.lastPosx = self.posx
        self.lastPosy = self.posy
        self.posx, self.posy = pygame.mouse.get_pos()
        
        if not self.careForMouse:
            self.careForMouse = self.posx!=self.lastPosx or self.posy!=self.lastPosy or self.clicked[0] or self.scrolly != 0
            
        
    def resetHeldInputs(self):
        heldEventAfter = []
        for event in self.heldEvents:
            if self.inputEvent(event, True):
                heldEventAfter.append(event)
        self.heldEvents = copy.copy(heldEventAfter)
    def rumble(self, lf, hf, dur):
        if joystick.get_init():
            joystick.rumble(lf, hf, dur)
#region INPUTS

inputs = InputSystem()

gameManager.input = inputs

inputs.setKey(pygame.K_SPACE, "Jump")
inputs.setButton(0, "Jump")

inputs.setKey(pygame.K_LEFT, "MoveLeft")
inputs.setButton(13, "MoveLeft")
inputs.setAxis(0, (-2, -0.1), "MoveLeft")
inputs.setHat(0, -1, "MoveLeft")

inputs.setKey(pygame.K_RIGHT, "MoveRight")
inputs.setButton(14, "MoveRight")
inputs.setAxis(0, (0.1, 2), "MoveRight")
inputs.setHat(0, 1, "MoveRight")

inputs.setButton(1, "Stomp")
inputs.setKey(pygame.K_a, "Stomp")

inputs.setKey(pygame.K_RCTRL, "Dash")
inputs.setKey(pygame.K_d, "Dash")
inputs.setButton(2, "Dash")

inputs.setKey(pygame.K_w, "Interact")
inputs.setButton(3, "Interact")

inputs.setKey(pygame.K_LSHIFT, "Boost") 
inputs.setAxis(5, (-0.5, 2), "Boost")

inputs.setKey(pygame.K_LCTRL, "Climb")
inputs.setAxis(4, (-0.5, 2), "Climb")

inputs.setAxis(1, (-2, -0.5), "ClimbUp")
inputs.setButton(11, "ClimbUp")
inputs.setKey(pygame.K_UP, "ClimbUp")
inputs.setHat(1, 1, "ClimbUp")

inputs.setAxis(1, (0.5, 2), "ClimbDown")
inputs.setButton(12, "ClimbDown")
inputs.setKey(pygame.K_DOWN, "ClimbDown")
inputs.setHat(1, -1, "ClimbDown")

inputs.setButton(4, "Restart1")
inputs.setButton(9, "Restart1")
inputs.setKey(pygame.K_s, "Restart1")

inputs.setButton(5, "Restart2")
inputs.setButton(10, "Restart2")
inputs.setKey(pygame.K_DOWN, "Restart2")

inputs.setButton(6, "Pause")
inputs.setButton(7, "Pause")
inputs.setKey(pygame.K_ESCAPE, "Pause")


inputs.setKey(pygame.K_F4, "frateup")
inputs.setKey(pygame.K_F5, "fratedown")

inputs.setKey(pygame.K_F2, "screenshot")

inputs.setKey(pygame.K_F9, "toggleBlocks")



inputs.setKey(pygame.K_UP, "UIUP")
inputs.setAxis(1, (-2, -0.8), "UIUP")
inputs.setButton(11, "UIUP")
inputs.setHat(1, 1, "UIUP")

inputs.setKey(pygame.K_DOWN, "UIDOWN")
inputs.setAxis(1, (0.8, 2), "UIDOWN")
inputs.setButton(12, "UIDOWN")
inputs.setHat(1, -1, "UIDOWN")

inputs.setKey(pygame.K_LEFT, "UILEFT")
inputs.setButton(13, "UILEFT")
inputs.setAxis(0, (-2, -0.8), "UILEFT")
inputs.setHat(0, -1, "UILEFT")

inputs.setKey(pygame.K_RIGHT, "UIRIGHT")
inputs.setButton(14, "UIRIGHT")
inputs.setAxis(0, (0.8, 2), "UIRIGHT")
inputs.setHat(0, 1, "UIRIGHT")

inputs.setKey(pygame.K_RETURN, "UIACCEPT")
inputs.setButton(0, "UIACCEPT")

inputs.setButton(1, "UIBACK")


stallFrames = 0
frameAdvance = False
slashHeld = False

#endregion INPUTS

#region UI


#region UISTYLE
settingsTextStyle = UISTYLE(fontSize=17, fontColour=WHITE, padding=20, borderWidth=10, borderRadius=20, hasBackground=True, colour=DARK_RAT, borderColour=LIGHT_RAT)
settingsTitleStyle = UISTYLE(fontSize=17, fontColour=WHITE, padding=20, hasBackground=False, hasShadow=True, shadowOffset=4)
settingBackgroundStyleA = UISTYLE(colour=LIGHT_RAT_TRANS, borderRadius=20)
settingBackgroundStyleB = UISTYLE(colour=PINK_RAT_TRANS, borderRadius=20)
settingHeaderStyleA = UISTYLE(colour=PINK_RAT, borderRadius=20)
settingHeaderStyleB = UISTYLE(colour=DARK_RAT, borderRadius=20)
settingsButtonStyle = UIBUTTONSTYLE(
    UISTYLE(fontSize=17, fontColour=WHITE, padding=20, borderWidth=10, borderRadius=20, hasBackground=True, colour=DEFAULT_BUTTON_COLOURS[0], borderColour=DARK_RAT),
    UISTYLE(fontSize=17, fontColour=WHITE, padding=20, borderWidth=10, borderRadius=20, hasBackground=True, colour=DEFAULT_BUTTON_COLOURS[1], borderColour=PINK_RAT),
    UISTYLE(fontSize=17, fontColour=WHITE, padding=20, borderWidth=10, borderRadius=20, hasBackground=True, colour=DEFAULT_BUTTON_COLOURS[2], borderColour=DARK_RAT),
    )
highlightedHatButtonStyle = UIBUTTONSTYLE(
    UISTYLE(fontSize=17, fontColour=WHITE, padding=20, borderWidth=10, borderRadius=20, hasBackground=True, colour=DEFAULT_BUTTON_COLOURS[0], borderColour=GOLD),
    UISTYLE(fontSize=17, fontColour=WHITE, padding=20, borderWidth=10, borderRadius=20, hasBackground=True, colour=DEFAULT_BUTTON_COLOURS[1], borderColour=PINK_RAT),
    UISTYLE(fontSize=17, fontColour=WHITE, padding=20, borderWidth=10, borderRadius=20, hasBackground=True, colour=DEFAULT_BUTTON_COLOURS[2], borderColour=DARK_RAT),
    )
mainMenuLockedButtonStyle = UISTYLE(True, SILVER, 10, 20, fontSize=20, fontColour=WHITE, padding=20, borderColour=GREY)
#endregion UISTYLE

# defaultButtonStyle = UISTYLE(DARK_RAT, 10, 20)
#region DEBUGUI
debugUi:UICanvas = UICanvas()
debugUi.addElement(UIText((0,0), "FPSText", "FPS:", style=UISTYLE(font="debug.ttf", fontSize=10, fontColour=BLACK, hasBackground=True, colour=WHITE, padding=8, borderColour=DARK_RAT)))
debugUi.getElementByTag("FPSText").setBG((255,255,255))

debugButtonStyle = UIBUTTONSTYLE(UISTYLE(True, DEFAULT_BUTTON_COLOURS[0], 10, 20, fontSize=10, fontColour=WHITE, padding=20))

debugStyle = UISTYLE(font="debug.ttf", fontSize=20, fontColour=BLACK, hasBackground=True, colour=WHITE, padding=0)
fullDebugUi:UICanvas = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
fullDebugUi.show = False
fullDebugUi.addElement(UIText((0,20), "x", "X:", style=debugStyle))
fullDebugUi.addElement(UIText((0,40), "y", "Y:", style=debugStyle))
fullDebugUi.addElement(UIText((0,60), "ctiles", "Collision Tiles:", style=debugStyle))
fullDebugUi.addElement(UIText((0,80), "stomp", "Stomp:", style=debugStyle))
fullDebugUi.addElement(UIText((0,100), "dtime", "DeltaTime:", style=debugStyle))
fullDebugUi.addElement(UIText((0,120), "speed", "Speed:", style=debugStyle))
fullDebugUi.addElement(UIText((0,160), "tframes", "Target Frames:", style=debugStyle))
fullDebugUi.addElement(UIText((0,180), "tiles", "Tiles:", style=debugStyle))

fullDebugUi.addElement(UIButton((100, 350), "fly mode", gameManager.toggleFlyMode, "FLY MODE", style=debugButtonStyle))

#endregion DEBUG UI

#region HUD
timerStyle = UISTYLE(font="rattimer.ttf", colour=(255,255,255, 150), hasBackground=True, fontSize=5, fontColour=BLACK)
hud:UICanvas = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
hud.show = False
hud.addElement(UIRect((0, h-20), "fullBoostBar", 200, 20, style=UISTYLE(colour=GREY, hasBackground=True)))
hud.addElement(UIRect((0, h-20), "boostBar", 100, 20, style=UISTYLE(colour=YELLOW)))
hud.addElement(UIRect((100, h-20), "boostBarCoins", 100, 20, style=UISTYLE(colour=ORANGE)))
hud.addElement(UIText((589,26), "timer", "00:00.00", style=timerStyle))
hud.getElementByTag("timer").show = False
hud.addElement(UIImage((84, 683), "fullBoost", [resources.uiAnimations["HUD"]["fullBoost"]]))
hud.addElement(UIImage((184, 683), "secondFullBoost", [resources.uiAnimations["HUD"]["fullBoost"]]))

hud.addElement(UIText((0,653), "coins", "Coins: 0/20", style=UISTYLE(fontSize=20, fontColour=BLACK, hasBackground=True, colour=WHITE, padding=6)))

#endregion HUD

#region PAUSE
uiPause:UICanvas = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiPause.show = False
uiPause.addElement(UIRect((0,0), "PauseBG", w, h, style=UISTYLE(colour=(100,100,100,100))))


pauseMenuButtonStyle = UIBUTTONSTYLE(
    UISTYLE(True, DEFAULT_BUTTON_COLOURS[0], 10, 20, fontSize=10, fontColour=WHITE, padding=20, borderColour=DARK_RAT),
    UISTYLE(True, DEFAULT_BUTTON_COLOURS[1], 10, 20, fontSize=10, fontColour=WHITE, padding=20, borderColour=PINK_RAT),
    UISTYLE(True, DEFAULT_BUTTON_COLOURS[2], 10, 20, fontSize=10, fontColour=WHITE, padding=20, borderColour=DARK_RAT)
    )
pauseMenuLockedButtonStyle = UISTYLE(fontSize=10, fontColour=WHITE, padding=20, borderWidth=10, borderRadius=20, hasBackground=True, colour=SILVER, borderColour=GREY)

uiPauseButtons = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiPauseButtons.show = False
uiPauseButtons.addElement(UIText((100,130), "PauseText", "PAUSE", style=UISTYLE(fontSize=50, padding=20, fontColour=WHITE, colour=PINK_RAT, borderRadius=10, hasBackground=True)))
uiPauseButtons.addElement(UIButton((100, 250), "back", gameManager.togglePause, "Continue", style=pauseMenuButtonStyle))
uiPauseButtons.addElement(UIButton((100, 320), "Restart Button", gameManager.quickRestart, "Restart", style=pauseMenuButtonStyle, locked=True, lockedStyle=pauseMenuLockedButtonStyle))
uiPauseButtons.addElement(UIButton((100, 390), "Settings Button", gameManager.openSettingsPause, "Settings", style=pauseMenuButtonStyle))
uiPauseButtons.addElement(UIButton((100, 460), "Controls Button", gameManager.showControlsPauseMenu, "Controls", style=pauseMenuButtonStyle))
uiPauseButtons.addElement(UIButton((100, 530), "MainMenu Button", gameManager.returnToMainMenu, "Main Menu", style=pauseMenuButtonStyle))
uiPauseButtons.addElement(UIButton((100, 600), "Hub Button", gameManager.goToHub, "Return to Hub", style=pauseMenuButtonStyle, locked=True, lockedStyle=pauseMenuLockedButtonStyle))
uiPauseButtons.addElement(UIButton((100, 670), "Feedback Button", gameManager.openFeedback, "Feedback", style=pauseMenuButtonStyle))


uiPauseButtons.makeMap({
    "back": {"down": "Restart Button", "up": "Feedback Button"},
    "Restart Button": {"down": "Settings Button", "up": "back"},
    "Settings Button": {"down": "Controls Button", "up": "Restart Button"},
    "Controls Button": {"down": "MainMenu Button", "up": "Settings Button"},
    "MainMenu Button": {"down": "Hub Button", "up": "Controls Button"},
    "Hub Button": {"down": "Feedback Button", "up": "MainMenu Button"},
    "Feedback Button": {"down": "back", "up": "Hub Button"}
})

#endregion PAUSE

#region hat

uiHat:UICanvas = UICanvas(inputs=inputs, audioPlayer=audioPlayer, canScroll=True)
uiHat.show = False

uiHat.addElement(UIRect((0, 100), "hatButtonBG", w/2, 621, style=settingBackgroundStyleA, lockScroll=True))
uiHat.addElement(UIRect((w/2, 100), "hatRatBG", w/2, 621, style=settingBackgroundStyleB, lockScroll=True))

uiHat.addElement(UIImage((706, 270), "ratPreview", [pygame.transform.scale(playerImages[0], (510, 510))], lockScroll=True))
uiHat.addElement(UIImage((706, 270), "ratPreviewLook", [pygame.transform.scale(pygame.image.load("ui/rat/hatPreviewRat.png").convert_alpha(), (510, 476))], lockScroll=True))
uiHat.getElementByTag("ratPreviewLook").show = False
uiHat.addElement(UIImage((706, -70), "hatPreview", [pygame.Surface((0,0))], lockScroll=True))

uiHat.addElement(UIRect((0, 0), "titleBG", w, 99, lockScroll=True, style=settingHeaderStyleA))
uiHat.addElement(UIText((40, 10), "TITLE", "Hats", lockScroll=True, style=settingsTitleStyle))
 
uiHat.addElement(UIImage((w-90,10), "ratBluePrints", resources.uiAnimations["bluePrints"], 6, lockScroll=True))

uiHat.addElement(UIButton((523, 100), "back", gameManager.whichCloseHats, "Back", lockScroll=True ,style=settingsButtonStyle))

uiHat.addElement(UIText((0, 320), "noHatsText", "You currently have not hats :(\n\n\nGetting S ranks and exploring\n\nwill gain you some hats!\n\n\nYour head looks pretty cold.\n\nSo you should hurry up!", style = settingsTitleStyle))
uiHat.addElement(UIImage((706, 270), "ratPreviewLookSad", [pygame.transform.scale(pygame.image.load("ui/rat/hatPreviewRatSad.png").convert_alpha(), (510, 476))], lockScroll=True))


uiHat.makeMap( # creates the map first, since the gameManager needs the map to add the new button to
    {
        "back": {"up": "none", "down": "none", "left": "none"}
    }
)
gameManager.addHat("none")
uiHat.getElementByTag("none").updateText("No Hat")

hatManager.loadHats()
uiHat.getElementByTag("noHatsText").show = len(hatManager.hats["hats"]) == 0
uiHat.getElementByTag("ratPreviewLookSad").show = len(hatManager.hats["hats"]) == 0

#endregion hat

#region MAINMENU
mainMenuButtonStyle = UIBUTTONSTYLE(
    UISTYLE(True, DEFAULT_BUTTON_COLOURS[0], 10, 20, fontSize=20, fontColour=WHITE, padding=20, borderColour=DARK_RAT),
    UISTYLE(True, DEFAULT_BUTTON_COLOURS[1], 10, 20, fontSize=20, fontColour=WHITE, padding=20, borderColour=PINK_RAT),
    UISTYLE(True, DEFAULT_BUTTON_COLOURS[2], 10, 20, fontSize=20, fontColour=WHITE, padding=20, borderColour=DARK_RAT)
    )

subtitleStyle = UISTYLE(fontSize=30, fontColour=WHITE, hasShadow=True, shadowOffset=6)

uiMainMenu:UICanvas = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiMainMenu.show = True
uiMainMenu.addElement(UIText((100,70), "TITLE", "Really Fast Rat", style=UISTYLE(fontSize=60, fontColour=WHITE, hasShadow=True, shadowOffset=12)))
uiMainMenu.addElement(UIText((100,170), "SUBTITLE", "INDEV VERSION - 0.0.5 - PLAYTEST I-B",  style=subtitleStyle))
uiMainMenu.addElement(UIButton((100, 250), "Start Button", gameManager.toggleLevelSelect, "Start", style = mainMenuButtonStyle))
uiMainMenu.addElement(UIButton((100, 350), "Settings Button", gameManager.openSettingsMainMenu, "Settings", style = mainMenuButtonStyle))
uiMainMenu.addElement(UIButton((100, 450), "controls", gameManager.whichShowControls, "Controls", style = mainMenuButtonStyle))
uiMainMenu.addElement(UIButton((100, 550), "hats", gameManager.whichOpenHats, "Hats", style = mainMenuButtonStyle, locked=False, lockedStyle=mainMenuLockedButtonStyle))
uiMainMenu.addElement(UIButton((100, 650), "back", gameManager.toggleShowQuit, "Quit Game", style = mainMenuButtonStyle))
uiMainMenu.addElement(UIButton((1000, 550), "Feedback Button", gameManager.openFeedback, "Feedback", style = mainMenuButtonStyle))

uiMainMenu.makeMap({
    "Start Button": {"up": "back", "down": "Settings Button", "right": "Feedback Button"},
    "Settings Button": {"up": "Start Button", "down": "controls", "right": "Feedback Button"},
    "controls": {"up": "Settings Button", "down": "hats", "right": "Feedback Button"},
    "hats": {"up": "controls", "down": "back", "right": "Feedback Button"},
    "back": {"up": "hats", "down": "Start Button", "right": "Feedback Button"},
    "Feedback Button": {"left": "Start Button"}
})

#https://forms.gle/Uez6tRceadLUjGgXA

uiMainMenu.addElement(UIImage((w-140, h-50), "ruby logo", [logo[2]]))


uiMainMenuQuit = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiMainMenuQuit.show = False
uiMainMenuQuit.addElement(UIText((100,100), "TITLE", "Are you sure you want to quit??", style=subtitleStyle))
uiMainMenuQuit.addElement(UIButton((100, 350), "quit", quitGame, "Quit Game", style = UIBUTTONSTYLE(
    UISTYLE(True, RED, 10, 20, fontSize=20, fontColour=WHITE, padding=20, borderColour=WHITE),
    UISTYLE(True, PINK, 10, 20, fontSize=20, fontColour=BLACK, padding=20, borderColour=RED),
    UISTYLE(True, DEFAULT_BUTTON_COLOURS[2], 10, 20, fontSize=20, fontColour=WHITE, padding=20, borderColour=DARK_RAT)
    )))
uiMainMenuQuit.addElement(UIButton((100, 450), "back", gameManager.toggleShowQuit, "Back To Game", style = mainMenuButtonStyle))

uiMainMenuQuit.addElement(UIImage((600, 400), "sad", resources.uiAnimations["sad"], fps = 10, style=UISTYLE(hasShadow=True, shadowColour=BLACK, shadowOffset=20)))

uiMainMenuQuit.makeMap({
    "quit": {"up": "back", "down": "back"},
    "back": {"up": "quit", "down": "quit"}
})


#endregion MAINMENU

#region SETTINGS
uiSettings:UICanvas = UICanvas(True, inputs=inputs, audioPlayer=audioPlayer, maxScroll=490)
uiSettings.show = False

uiSettings.addElement(UIRect((0, 100), "soundBG", w, 409, style=settingBackgroundStyleA))
uiSettings.addElement(UIText((40, 100), "soundTitle", "Sound Settings", style=settingsTitleStyle))
uiSettings.addElement(UIButton((40, 170), "MusicUp", gameManager.increaseMusicVolume, "Increase Music Volume",style=settingsButtonStyle))
uiSettings.addElement(UIText((490,205), "musicVolume", f"{s.settings['musicVolume']}%",style=settingsTextStyle))
uiSettings.addElement(UIButton((40, 240), "MusicDown", gameManager.decreaseMusicVolume, "Decrease Music Volume",style=settingsButtonStyle))

uiSettings.addElement(UIButton((40, 340), "SFXUp", gameManager.increaseSoundVolume, "Increase Sound Volume",style=settingsButtonStyle))
uiSettings.addElement(UIText((490,375), "soundVolume", f"{s.settings['sfxVolume']}%",style=settingsTextStyle))
uiSettings.addElement(UIButton((40, 410), "SFXDown", gameManager.decreaseSoundVolume, "Decrease Sound Volume",style=settingsButtonStyle))

uiSettings.addElement(UIRect((0, 510), "graphicsBG", w, 499, style=settingBackgroundStyleB))
uiSettings.addElement(UIText((40, 510), "graphicsTitle", "Graphics Settings", style=settingsTitleStyle))

uiSettings.addElement(UIButton((40, 610), "bgToggle", gameManager.toggleBG, "Background Detail",style=settingsButtonStyle))
uiSettings.addElement(UIText((490,610), "bgDetail", f"{gameManager.bgDetailLevels[s.settings['backgroundDetail']]}",style=settingsTextStyle))

uiSettings.addElement(UIButton((40, 710), "particleToggle", gameManager.toggleParticles, "Show Particles",style=settingsButtonStyle))
uiSettings.addElement(UIText((490, 710), "particleToggleStatus", f"{'On' if s.settings['particles'] else 'Off'}",style=settingsTextStyle))

uiSettings.addElement(UIButton((40, 810), "animationToggle", gameManager.toggleParticles, "Animate Tiles",style=settingsButtonStyle))
uiSettings.addElement(UIText((490, 810), "animationToggleStatus", f"{'On' if s.settings['particles'] else 'Off'}",style=settingsTextStyle))

uiSettings.addElement(UIButton((40, 910), "fullscreenToggle", gameManager.toggleFullscreen, "Fullscreen",style=settingsButtonStyle))
uiSettings.addElement(UIText((490, 910), "fullscreenToggleStatus", f"{'Off'}",style=settingsTextStyle))

uiSettings.addElement(UIRect((0, 1010), "gamplayBG", w, 200, style=settingBackgroundStyleA))
uiSettings.addElement(UIText((40, 1010), "gameplayTitle", "Gameplay Settings", style=settingsTitleStyle))

uiSettings.addElement(UIButton((40, 1110), "quickRestartToggle", gameManager.toggleQuickRestart, "Quick Restart Input",style=settingsButtonStyle))
uiSettings.addElement(UIText((490, 1110), "quickRestartToggleStatus", f"{'On' if s.settings['quickRestartButton'] else 'Off'}",style=settingsTextStyle))

uiSettings.addElement(UIButton((w-410, 100), "back", gameManager.whichCloseSettings, "Save Settings", lockScroll=True ,style=settingsButtonStyle))

uiSettings.addElement(UIRect((0, 0), "titleBG", w, 99, lockScroll=True, style=settingHeaderStyleA))
uiSettings.addElement(UIText((40, 10), "TITLE", "Settings", lockScroll=True, style=settingsTitleStyle))
 
uiSettings.addElement(UIImage((w-90,10), "ratBluePrints", resources.uiAnimations["bluePrints"], 6, lockScroll=True))



uiSettings.makeMap({
    "back": {"left": "MusicUp"},
    "MusicUp": {"up": "quickRestartToggle", "down": "MusicDown", "right": "back"},
    "MusicDown": {"up": "MusicUp", "down": "SFXUp", "right": "back"},
    "SFXUp": {"up": "MusicDown", "down": "SFXDown", "right": "back"},
    "SFXDown": {"up": "SFXUp", "down": "bgToggle", "right": "back"},
    "bgToggle": {"up": "SFXDown", "down": "particleToggle", "right": "back"},
    "particleToggle": {"up": "bgToggle", "down": "animationToggle", "right": "back"},
    "animationToggle": {"up": "particleToggle", "down": "fullscreenToggle", "right": "back"},
    "fullscreenToggle": {"up": "animationToggle", "down": "quickRestartToggle", "right": "back"},
    "quickRestartToggle": {"up": "fullscreenToggle", "down": "MusicUp", "right": "back"}
})

#endregion Settings


#region CONTROLS
uiControls:UICanvas = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiControls.show = False

uiControls.addElement(UIRect((0, 100), "controlsBg", w, h-100, style=settingBackgroundStyleB))

uiControls.addElement(UIRect((0, 0), "titleBG", w, 99, lockScroll=True, style=settingHeaderStyleB))
uiControls.addElement(UIText((40, 10), "TITLE", "Controls", lockScroll=True, style=settingsTitleStyle))

uiControls.addElement(UIButton((1035, 100), "reload", reloadController, "Connect\n\nController",style=settingsButtonStyle))
uiControls.addElement(UIButton((1158, 196), "back", gameManager.whichCloseControls, "Back",style=settingsButtonStyle))
uiControls.addElement(UIButton((1158, 258), "toggle", gameManager.toggleControllerVisual, "Next",style=settingsButtonStyle))
 
uiControls.addElement(UIImage((w-90,10), "ratBluePrints", resources.uiAnimations["bluePrints"], 6, lockScroll=True))

uiControls.makeMap({
    "reload": {"up": "toggle", "down": "back"},
    "back": {"down": "toggle", "up": "reload"},
    "toggle": {"up": "back", "down": "reload"}
})


uiControlsXbox:UICanvas = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiControlsXbox.show = False
uiControlsXbox.addElement(UIImage((-170,80), "xbox", [resources.uiAnimations["controlLayouts"]["xbox"]], 6))
uiControlsXbox.addElement(UIText((159, 131), "climb", "CLIMB (HOLD)",style=settingsTextStyle))
uiControlsXbox.addElement(UIText((707, 131), "run", "RUN (HOLD)",style=settingsTextStyle))
uiControlsXbox.addElement(UIText((36, 457), "move", "MOVE",style=settingsTextStyle))
uiControlsXbox.addElement(UIText((772, 305), "dash", "DASH",style=settingsTextStyle))
uiControlsXbox.addElement(UIText((1013, 313), "stomp", "STOMP",style=settingsTextStyle))
uiControlsXbox.addElement(UIText((892, 641), "jump", "JUMP",style=settingsTextStyle))

uiControlsPlaystation:UICanvas = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiControlsPlaystation.show = False
uiControlsPlaystation.addElement(UIImage((-170,80), "ps", [resources.uiAnimations["controlLayouts"]["ps"]], 6))
uiControlsPlaystation.addElement(UIText((159, 131), "climb", "CLIMB (HOLD)",style=settingsTextStyle))
uiControlsPlaystation.addElement(UIText((707, 131), "run", "RUN (HOLD)",style=settingsTextStyle))
uiControlsPlaystation.addElement(UIText((36, 457), "move", "MOVE",style=settingsTextStyle))
uiControlsPlaystation.addElement(UIText((772, 305), "dash", "DASH",style=settingsTextStyle))
uiControlsPlaystation.addElement(UIText((1013, 313), "stomp", "STOMP",style=settingsTextStyle))
uiControlsPlaystation.addElement(UIText((892, 641), "jump", "JUMP",style=settingsTextStyle))

uiControlsPC:UICanvas = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiControlsPC.show = False
uiControlsPC.addElement(UIImage((-170,80), "pc", [resources.uiAnimations["controlLayouts"]["pc"]], 6))
uiControlsPC.addElement(UIText((320, 332), "climb", "CLIMB (HOLD)",style=settingsTextStyle))
uiControlsPC.addElement(UIText((320, 232), "run", "RUN (HOLD)",style=settingsTextStyle))
uiControlsPC.addElement(UIText((320, 132), "move", "MOVE",style=settingsTextStyle))
uiControlsPC.addElement(UIText((320, 532), "dash", "DASH",style=settingsTextStyle))
uiControlsPC.addElement(UIText((320, 632), "stomp", "STOMP",style=settingsTextStyle))
uiControlsPC.addElement(UIText((320, 432), "jump", "JUMP",style=settingsTextStyle))

#endregion CONTROLS


#region LEVELTITLE
uiLevelTitle:UICanvas = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiLevelTitle.show = False
uiLevelTitle.addElement(UIImage((-562, 125), "bg", [resources.uiAnimations["levelName"]["bg"]], 1))
uiLevelTitle.addElement(UIText((100, h+400), "lvlName", "LEVEL NAME", style=UISTYLE(fontColour=BLACK, fontSize=40)))

#endregion LEVELTITLE

#region RESULTS
uiResults:UICanvas = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiResults.show = False
uiResults.addElement(UIRect((0,0), "resultBG", w, h, style=UISTYLE(colour=(100,100,100,100))))
uiResults.addElement(UIText((0,0), "ResultText", "RESULTS:", style=UISTYLE(fontSize=50, padding=20, fontColour=WHITE, colour=PINK_RAT, borderRadius=10)))
uiResults.addElement(UIRect((w-400,0), "timesBG", 400, 277, style=UISTYLE(colour=(100,100,100,100))))

uiResults.addElement(UIText((w-400,0), "s", "S RANK: 00:00", style=UISTYLE(fontSize=10, padding=20, fontColour=BLACK)))
uiResults.addElement(UIText((w-400,50), "a", "A RANK: 00:00", style=UISTYLE(fontSize=10, padding=20, fontColour=BLACK)))
uiResults.addElement(UIText((w-400,100), "b", "B RANK: 00:00", style=UISTYLE(fontSize=10, padding=20, fontColour=BLACK)))
uiResults.addElement(UIText((w-400,150), "c", "C RANK: 00:00", style=UISTYLE(fontSize=10, padding=20, fontColour=BLACK)))
uiResults.addElement(UIText((w-400,200), "d", "D RANK: 00:00", style=UISTYLE(fontSize=10, padding=20, fontColour=BLACK)))

uiResults.addElement(UIImage((w-400, 338), "rank", [resources.uiAnimations["rankings"]["s"]], 1))

uiResults.addElement(UIButton((w-600, 520), "try again", gameManager.quickRestart, "Try Again", style=pauseMenuButtonStyle))
uiResults.addElement(UIButton((w-600, 590), "hub", gameManager.goToHub, "Return To Hub", style=pauseMenuButtonStyle))
uiResults.addElement(UIButton((w-600, 660), "main menu", gameManager.returnToMainMenu, "Main Menu", style=pauseMenuButtonStyle))

uiResults.addElement(UIText((0,300), "timer", "00:00.00", style=UISTYLE(font="rubfont.ttf", colour=(255,255,255, 150), hasBackground=True, fontSize=35, fontColour=BLACK)))

uiResults.makeMap({
    "try again": {"down": "hub", "up": "main menu"},
    "hub": {"down": "main menu", "up": "try again"},
    "main menu": {"down": "try again", "up": "hub"}
})

#endregion RESULTS

#endregion UI

debug = 1
debugHeld = False

targetFrames = 60

titleLerpStall = 180
titleLerpStage = 0

waiting = False

#@profile
def main():
    
    # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    global posx, posy, clicked, pauseHeld, scrolly, keys, debugHeld, targetFrames, frameAdvance, stompHeld, spaceHeld, titleLerpStall, titleLerpStage, debug, slashHeld, stallFrames, deltaTime, worldX, worldY, run, useFullScreen, waiting
    gameManager.update()
    scrolly = 0
    inputs.scrolly = scrolly
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEWHEEL:
            scrolly = event.y
            inputs.scrolly = scrolly
        elif event.type == pygame.VIDEORESIZE:
            # This event is triggered when the win is resized
            #w, h = event.w, event.h
            pass
        elif event.type == pygame.JOYDEVICEREMOVED:
            reloadController()
            inputs.careForMouse = True

        elif event.type == pygame.JOYDEVICEADDED:
            reloadController()
            inputs.careForMouse = False
    
    for clickState in range(len(inputs.clickDown)):
        if inputs.clickDown[clickState]:
            inputs.clickDown[clickState] = clicked[clickState]
                
    inputs.update()
    inputs.scrolly = scrolly
    
    #mouse getters
    clicked = pygame.mouse.get_pressed(num_buttons=3)
    inputs.clicked = clicked

    level.trimLevel()
    
    
    
    if not uiLevelTitle.getElementByTag("lvlName").lerp:
        if titleLerpStall > 0:
            titleLerpStall -=1
        else:
            uiLevelTitle.show = False
            
    else:
        uiLevelTitle.update()
    
    level.checkCollision(player.charRect, True, [18])
    
    
    keys = pygame.key.get_pressed()

    if pauseHeld:
        pauseHeld = inputs.inputEvent("Pause")

    if not gameManager.pause and gameManager.inGame:

        if stompHeld:
            stompHeld = inputs.inputEvent("Stomp")
        if spaceHeld:
            spaceHeld = inputs.inputEvent("Jump")

        if not uiResults.show: 
            player.update()
            
            
            player.jumpPower = 11

            if ((inputs.inputEvent("MoveLeft") and not inputs.inputEvent("MoveRight")) or (inputs.inputEvent("MoveRight") and not inputs.inputEvent("MoveLeft")))  and not player.lockMovement:
                if inputs.inputEvent("MoveLeft") and not inputs.inputEvent("MoveRight"):
                    player.changeXVel(gameManager.speed/10, False)
                if inputs.inputEvent("MoveRight") and not inputs.inputEvent("MoveLeft"):
                    player.changeXVel(gameManager.speed/10, True)
            elif player.xVel > 0:
                player.xVel-=player.decelSpeed
                player.changeXVel(0, True)
                player.boostDirection = 0
            elif player.xVel < 0:
                player.xVel+=player.decelSpeed
                player.changeXVel(0, False)
                player.boostDirection = 0
                
                
            if s.settings['quickRestartButton']:
                if inputs.inputEvent("Restart1") and inputs.inputEvent("Restart2"):
                    gameManager.quickRestart()


        if keys[pygame.K_r]:
            if keys[pygame.K_LCTRL]:
                if keys[pygame.K_LSHIFT]:
                    level.changeLevel(True, True)
                    debugLog.append(DebugLogText("Full Reload"))
                    player.reset(False)
                    playerImages = resources.reloadPlayerImages(player.hat)
                else:
                    debugLog.append(DebugLogText("Advanced Reload"))
                    level.changeLevel(False, True)
                    player.reset(False)
        
        if keys[pygame.K_t] and keys[pygame.K_LCTRL]:
            worldX = input("enter world x: ")
            worldY = input("enter world y: ")
            level.changeLevel(True, True)

        
        
        gameManager.speed = 3
        
        level.updateTiles()
        level.singleUpdateTiles()
        
        # for tile in level.levels:
        #     tile.singleUpdate()
        
        uiResults.update()
    
    elif gameManager.mainMenu:
        
        uiMainMenu.update()
        uiMainMenuQuit.update()
        uiControls.update()
        uiHat.update()
    
    elif gameManager.settingsMenu:
        
        uiSettings.update()
        
        
        
    elif gameManager.pause:
        
        uiPause.update()
        
        uiPauseButtons.update()
        uiControls.update()
        
        if keys[pygame.K_r]:
            reloadController()
        
    if inputs.inputEvent("Pause") and not pauseHeld and gameManager.inGame and not uiResults.show:
        gameManager.togglePause()
        pauseHeld = True

            
    
    if debugHeld:
        debugHeld = keys[pygame.K_F3] or keys[pygame.K_F11]
    if keys[pygame.K_F3] and not debugHeld:
        debug += 1
        debugHeld = True
        if debug == 4:
            debug = 0
            
    if keys[pygame.K_F11] and not debugHeld:
        debugHeld = True
        gameManager.toggleFullscreen()

    
    if inputs.inputEvent("frateup", False):
        targetFrames+=10
    elif inputs.inputEvent("fratedown", False):
        targetFrames-=10
        if targetFrames <= 0: targetFrames = 10
    

    
    
    if (keys[pygame.K_BACKSLASH] and not slashHeld) or frameAdvance:
        slashHeld = True
        waiting = True
        while waiting:
            deltaTime = 1
            redrawScreen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitGame()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSLASH] and not slashHeld:
                waiting = False
            if waiting:
                slashHeld = keys[pygame.K_BACKSLASH]
            if keys[pygame.K_z] and not frameAdvance:
                waiting = False
                frameAdvance = True
            if not keys[pygame.K_z]:
                frameAdvance = False
            if keys[pygame.K_x]:
                frameAdvance = True
                stallFrames+=1
                if stallFrames == 5:
                    waiting = False
                    stallFrames = 0

    slashHeld = keys[pygame.K_BACKSLASH]
    
    if inputs.inputEvent("screenshot", False):
        if not os.path.exists("screenshots"): os.makedirs("screenshots")
        screenshotName = str(int(time.time())) + ".png"
        pygame.image.save(win, f"screenshots/{screenshotName}")
        debugLog.append(DebugLogText(f"Game Screenshotted -> {screenshotName}", 120, "cam"))
    
    if keys[pygame.K_F7]:
        p = Particle(player.x, player.y, 1, 1, 20, 20, 120, RED)
        gameManager.addParticle(p)
    if keys[pygame.K_F8] and not debugHeld:
        debugHeld = True
        gameManager.collectables += 1
        

    gameManager.finalUpdate()
        
        
# Main game loop
while run:
    main()
    redrawScreen()
        
    
    # Set the framerate
    deltaTime = clock.tick(targetFrames)* 0.001 * 60
    if deltaTime >= 2: deltaTime = 2
    deltaTime = 1
        
quitGame()