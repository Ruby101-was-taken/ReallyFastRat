

worldX, worldY = 0,0

collisionTiles = 0



import pygame, random, os, csv, copy, time
import math as maths
import threading
import webbrowser

from animation import Animation

from audioSource import AudioSource

from colours import *

from ratFacts import facts

from jsonParse import *
from sign import *

from settings import s


from entity import Entity


from profiler import *

os.system("cls")


useFullScreen = False # change to load on fullscreen or not

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

# Set up the display
if useFullScreen:
    window = pygame.display.set_mode((w, h), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF | pygame.HWSURFACE)
else:
    window = pygame.display.set_mode((w, h), pygame.RESIZABLE | pygame.SCALED | pygame.DOUBLEBUF | pygame.HWSURFACE)
    
    
    
from resources import * #load all images from the external python file

from tiles import *

class noJoystick:
    def get_init(self):
        return False
    def get_button(self, num):
        return False
    def get_axis(self, num):
        return False
    def get_hat(self, num):
        return (0,0)

def reloadController():
    global joystick, win
    num_joysticks = pygame.joystick.get_count()
    print(num_joysticks)
    if num_joysticks > 0:
        if num_joysticks == 1:
            joystick = pygame.joystick.Joystick(0)
            print(joystick.get_name())
            joystick.rumble(1, 1, 1000)
        else:
            from extraControllers import getController
            joystick = pygame.joystick.Joystick(getController(num_joysticks, pygame.joystick))
            joystick.rumble(1, 1, 1000)
        joystick.init()
    else:
        print("No controllers found.")
        joystick = noJoystick()
        
    
    if useFullScreen:
        window = pygame.display.set_mode((w, h), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF | pygame.HWSURFACE)
    else:
        window = pygame.display.set_mode((w, h), pygame.RESIZABLE | pygame.SCALED | pygame.DOUBLEBUF | pygame.HWSURFACE)
        
reloadController()

isXboxController = False
if joystick.get_init():
    if "xbox" in joystick.get_name().lower():
        isXboxController = True


    
pygame.display.set_caption("Really Fast Rat")
pygame.display.set_icon(pygame.image.load('icon.png'))

logo=[pygame.image.load('logo/logosubless.png'), pygame.image.load('logo/logoSUB.png'), pygame.image.load('logo/logoDecorSmol.png')]




loadingTexts = ["LOADING IMAGES", "LOADING UI", "LOADING SOUNDS"]


# Set up fonts
smallFont = pygame.font.SysFont("arial", 20)
smallerFont = pygame.font.SysFont("arial", 15)
bigFont = pygame.font.SysFont("arial", 45)

loadingFactFont = pygame.font.SysFont("arial", 30)

# Set up timer
clock = pygame.time.Clock()

win = pygame.Surface((w, h))

logoPos = 0
logoSubPos = pygame.math.Vector2()
logoSubPos.x = -401
logoSubPos.y = h+146

# logoScreen = True
# delay = 60
# while logoScreen:
#     win.fill(LOGORED)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             run = False
#             quit()
#         elif event.type == pygame.VIDEORESIZE:
#             # This event is triggered when the win is resized
#             w, h = event.w, event.h
#     delay-=1
#     if delay <= 0:
#         if logoPos < 473:
#             logoPos = pygame.math.lerp(logoPos, 473, 0.05)
#         win.blit(logo[0], (logoPos, 313))
#     if delay <= -60:
#         if logoSubPos.x < 511 and logoSubPos.y > 318:
#             logoSubPos.x = pygame.math.lerp(logoSubPos.x, 511, 0.05)
#             logoSubPos.y = pygame.math.lerp(logoSubPos.y, 318, 0.045)
#         win.blit(logo[1], logoSubPos)
        
#     logoScreen = delay > -400
#     window.blit(win, (0,0)) 
#     pygame.display.flip()

# del delay, logoScreen, logoPos, logoSubPos





def resliceImages(tileType:str):
    tileImages.groundImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/ground.png").convert_alpha(), tileSize, tileSize)
    tileImages.spikeImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/spikeTiles.png").convert_alpha(), tileSize, tileSize)
    tileImages.bridgeImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/bridgeTiles.png").convert_alpha(), tileSize, tileSize)
    tileImages.objectImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/objectTiles.png").convert_alpha(), tileSize, tileSize)
    tileImages.groundBImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/groundB.png").convert_alpha(), tileSize, tileSize)
    tileImages.groundCImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/groundC.png").convert_alpha(), tileSize, tileSize)
    tileImages.groundDImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/groundD.png").convert_alpha(), tileSize, tileSize)

    tileImages.backGroundAImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/backGroundA.png").convert_alpha(), tileSize, tileSize)
    tileImages.backGroundBImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/backGroundB.png").convert_alpha(), tileSize, tileSize)
    tileImages.backGroundCImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/backGroundC.png").convert_alpha(), tileSize, tileSize)
    tileImages.backGroundDImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/backGroundD.png").convert_alpha(), tileSize, tileSize)
    
    tileImages.movingPlatformImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/movingPlatform.png").convert_alpha(), tileSize, tileSize)


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

textBoxFont = pygame.font.Font("font.ttf", 25)
endTitle = pygame.font.Font("font.ttf", 50)
endSubTitle = pygame.font.Font("font.ttf", 25)

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
        
        self.bgDetailLevels = ["None", "Min", "Max"]
        
        self.timer = 0
        self.timeString = ""
        
        self.timerOn = False
        
        self.flyMode = False
        
        
        self.collectables = 0
        self.collectablesLast = 0
        self.collectablesForNextLevel = 20
        
    def update(self):
        if self.collectablesLast != self.collectables:
            if self.collectables >= self.collectablesForNextLevel:
                self.collectables = 0
                player.levelUp()
            hud.getElementByTag("coins").updateText(f"Coins: {self.collectables}/{self.collectablesForNextLevel}")
            
        self.collectablesLast = self.collectables
        
        if self.timerOn:
            self.timer+=1
        # Calculate total seconds
        totalSeconds = self.timer // 60
       
        self.timeString = self.intToTime(totalSeconds)
        hud.getElementByTag("timer").updateText(self.timeString)
        
        if self.flyMode:
            player.superBoostCoolDown = 0
            player.kTime = 10
            
        
    def intToTime(self, num, includeCenti = True) -> str: 
        # Calculate minutes and remaining seconds
        minutes = num // 60
        seconds = num % 60
        
        # Calculate centiseconds
        if includeCenti: centiseconds = (self.timer % 60) * 100 // 60
        else: centiseconds = 0
        
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
            uiPause.getElementByTag("WorldText").updateText(f"{worldX} - {worldY}")
        else:
            if uiSettings.show or uiControls.show:
                self.closeSettingPause()
    def toggleMainMenu(self):
        self.mainMenu = not self.mainMenu
        uiMainMenu.show = self.mainMenu
    def toggleLevelSelect(self):
        audioPlayer.playSound(sounds["menuChange"])
        audioPlayer.playSound(sounds["rat"])
        self.toggleMainMenu()
        self.inGame = True
        hud.show = True
        level.changeLevel()
    
    def openFeedback(self):
        webbrowser.open("https://forms.gle/Uez6tRceadLUjGgXA") 
    
    def openSettings(self):
        self.settingsMenu = True
        
        uiSettings.show = True
        
        
        
        
    def closeSettings(self):
        self.settingsMenu = False
        uiSettings.show = False
        uiSettings.resetScroll()
        
        debugLog.append(DebugLogText("Settings Saved", 60))
        
        s.updateSettings()
        
        
    def openSettingsMainMenu(self):
        self.toggleMainMenu()
        uiMainMenuSettings.show = True
        uiMainMenuSettingsScroll.show = True
        
        
        self.openSettings()
        
    def closeSettingMainMenu(self):
        self.toggleMainMenu()
        uiMainMenuSettings.show = False
        uiMainMenuSettingsScroll.show = False
        uiMainMenuSettingsScroll.resetScroll()
        
        audioPlayer.playMusic(MusicSource(f"title.wav"), s.settings["musicVolume"]/100)
        audioPlayer.playSound(sounds["menuChange"])
        audioPlayer.playSound(sounds["rat"])
        
        self.closeSettings()
        
    def openSettingsPause(self):
        uiPauseSettings.show = True
        uiPauseButtons.show = False
        
        
        self.openSettings()
        
    def closeSettingPause(self):
        uiPauseSettings.show = False
        uiPauseButtons.show = self.pause
        audioPlayer.playSound(sounds["menuChange"])
        audioPlayer.playSound(sounds["rat"])
        
        uiControls.show = False
        uiControlsPause.show = False
        uiControlsXbox.show = False
        
        self.closeSettings()
        
    def changeMusicVolume(self):
        uiSettings.getElementByTag("musicVolume").updateText(f"{s.settings['musicVolume']}%")
        audioPlayer.music.set_volume(s.settings['musicVolume'] /100)
        
                
    def increaseMusicVolume(self):
        s.increaseMusicVolume()
        self.changeMusicVolume()
    def decreaseMusicVolume(self):
        s.decreaseMusicVolume()
        self.changeMusicVolume()
        
    def toggleBG(self):
        s.toggleBG()
        uiSettings.getElementByTag("bgDetail").updateText(f"{self.bgDetailLevels[s.settings['backgroundDetail']]}")
        
        uiMainMenuSettingsScroll.getElementByTag("bgDetailImg").changeImages([uiAnimations["bgDetail"][s.settings["backgroundDetail"]]])
        
    def toggleDrawThread(self):
        s.toggleDrawThread()
        uiSettings.getElementByTag("threadText").updateText(f"{s.settings['drawOnThread']}")
        
    def showControls(self):
        audioPlayer.playSound(sounds["menuChange"])
        audioPlayer.playSound(sounds["rat"])
        uiControls.show = True
        uiSettings.show = False
        uiControlsXbox.show = True
    def hideControls(self):
        audioPlayer.playSound(sounds["menuChange"])
        audioPlayer.playSound(sounds["rat"])
        uiControls.show = False
        uiSettings.show = True
        uiControlsXbox.show = False
        
    def showControlsMainMenu(self):
        uiMainMenuSettings.show = False
        uiMainMenuSettingsScroll.show = False
        uiControlsMainMenu.show = True
        
        self.showControls()
    def hideControlsMainMenu(self):
        uiMainMenuSettings.show = True
        uiMainMenuSettingsScroll.show = True
        uiControlsMainMenu.show = False
        
        self.hideControls()
        
    def showControlsPauseMenu(self):
        uiPauseSettings.show = False
        uiControlsPause.show = True
        
        self.showControls()
    def hideControlsPauseMenu(self):
        uiPauseSettings.show = True
        uiControlsPause.show = False
        
        self.hideControls()
        
    def nextLevel(self):
        global worldX, worldY
        worldX = level.levelInfo["nextLevel"]["x"]
        worldY = level.levelInfo["nextLevel"]["y"]
        
        
        self.closeResults()
        
    def closeResults(self):
        uiResults.show = False
        hud.show = True
        level.changeLevel(True, True)
        
    def toggleFlyMode(self):
        self.flyMode = not self.flyMode
        


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
        
        self.hat = "top"
        
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
        try:
            hud.getElementByTag("fullBoostBar").updateSize(200 + (100*abs(self.minCoinCoolDown/self.maxBoostCoolDown)), 20)
        except NameError:
            pass
        
    def changeX(self, speed): 
        #self.x+=speed
        
        walled = False
        velSign = sign(self.xVel)
        
        for i in range(int(abs(speed*2)//20)):
            self.x += sign(speed) * 20
            
            level.levelPosx = self.x
            
            
            if level.checkCollision(self.charRect):
                self.wallCheck(velSign)
                walled = True
        
        if abs(int(speed)*2)%20 > 0:
            self.x += (int(speed)*2)%(20 * sign(speed))
            
            level.levelPosx = self.x
            
            
            if level.checkCollision(self.charRect):
                self.wallCheck(velSign)
                walled = True
        
            
        
        
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
        
        
        
    def wallCheck(self, velSign):
        
        movedUp = False
        
        for i in range(10):
            level.levelPosy-=1
            if not level.checkCollision(self.charRect) and not movedUp:
                level.levelPosx+=velSign
                movedUp = True
                break
        
        if not movedUp:
            level.levelPosy+=10
            self.xVel = 0
            
            while level.checkCollision(self.charRect):
                self.x-= 1*velSign
                level.levelPosx = self.x
                
            if (inputs.inputEvent("Jump", False)) and self.wallJumpDelay == 0 and self.kTime == 0:
                self.wallJumped = True
                self.yVel = -10
                self.xVel = 10*-velSign
                self.bounce = False
            
            elif (inputs.inputEvent("Climb")):
                self.bounce = False
                self.yVel = 0
                self.climbedLastFrame=True

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
                    
        



    def changeXVel(self, speed, isRight):
        
        fullDebugUi.getElementByTag("speed").updateText("Speed: " + str(speed))
        
        self.wallJumped = False
        
        maxSpeed = self.maxSpeed        
        maxBoost = self.maxBoost
        
        boostButton = inputs.inputEvent("Boost") and level.levelInfo["canRun"]
            
        if not self.stomp:   
            self.isRight = isRight
            if isRight:
                self.xVel += speed
                if self.xVel > maxSpeed and not (boostButton or self.homeTo!=(0,0)):
                    self.xVel -= speed
                    if self.xVel > maxSpeed:
                        self.xVel-=self.decelSpeed      
                elif self.xVel > maxBoost and (boostButton or self.homeTo!=(0,0)):
                    self.xVel -= speed*3
                    if self.xVel > maxBoost:
                        self.xVel-=self.decelSpeed      
            elif not isRight:
                self.xVel -= speed
                if self.xVel < -maxSpeed and not (boostButton or self.homeTo!=(0,0)):
                    self.xVel += speed
                    if self.xVel < -maxSpeed:
                        self.xVel+=self.decelSpeed      
                elif self.xVel < -maxBoost and (boostButton or self.homeTo!=(0,0)):
                    self.xVel += speed*3
                    if self.xVel < -maxBoost:
                        self.xVel+=self.decelSpeed         
            self.xVel = round(self.xVel,2)
            if str(abs(self.xVel))[:3] == "0.1" or str(abs(self.xVel))[:3] == "0.0":
                self.xVel = 0
        else:
            self.xVel = 0


        if abs(self.xVel) > self.terminalVelocityX:
            self.xVel = self.terminalVelocityX*self.getDirNum()

        self.changeX((self.xVel)+sign(self.xVel))
        
        
    def gravity(self):
        if self.homeTo != (0,0):
            self.homingCoolDown-=1
            if self.homingCoolDown==0:
                self.homeTo=(0,0)
        level.levelPosy = round(level.levelPosy, 2)
        if level.levelPosy > level.lowestPoint:
            self.die()
            pass
        for i in range(int(self.yVel)):
            self.y+=deltaTime
            level.levelPosx, level.levelPosy = self.x, self.y
            if level.checkCollision(self.charRect):
                self.yVel = 0
                self.jumpsLeft = 2
                self.stomp = False
                player.decelSpeed = 0.2
                level.levelPosy = self.y
                self.homeTo = (0,0)
                break
            
        for i in range(-int(self.yVel)):
            self.y-=deltaTime
            level.levelPosx, level.levelPosy = self.x, self.y
            self.checkCeiling()
            
        if not level.checkCollision(self.charRect):
            self.yVel+=0.5*deltaTime
            if self.yVel > self.terminalVelocityY*deltaTime:
                self.yVel = self.terminalVelocityY*deltaTime
            self.kTime -= 1
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
                    self.yVel=+1
                    self.y+=1
                    level.levelPosy = self.y
                    self.touchGround=False
                    self.kTime = 0
                else:
                    self.y-=0.1
                    level.levelPosy = self.y
                    self.touchGround = level.checkCollision(self.charRect)
                    self.kTime = defaultKTime
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
                        self.jumpsLeft = 2
                else:
                    level.levelPosy+=int(self.yVel)+1
                    if self.semied:
                        self.kTime = defaultKTime
                    self.semied = False
                level.levelPosy-=1
                self.y = level.levelPosy
            elif self.semied and not inputs.inputEvent("Jump"):
                self.kTime = defaultKTime
                self.semied = False
            elif self.semied:
                self.semied = False




        level.checkCollision(self.charRect, True, [2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 23, 24, 26, 29, 30])
        
        global stompHeld
        if not self.climbedLastFrame and self.kTime < 8:
            if inputs.inputEvent("Stomp") and not stompHeld and not self.climbedLastFrame:
                self.stomp = True
                self.yVel = 20
                stompHeld = True
                
                self.stompVel = self.xVel + 5*sign(self.xVel)




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

    def process(self):
        
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
            
            coolDownToRemove = self.maxBoostCoolDown
            if self.superBoostCoolDownCoins <= 0:
                self.superBoostCoolDownCoins += coolDownToRemove
                coolDownToRemove = 0
            elif self.superBoostCoolDown <= 0:
                self.superBoostCoolDown += coolDownToRemove
                coolDownToRemove = 0
            
            
            self.homeTo = (0,0)
            self.stomp = False
            if self.yVel > -3:
                self.yVel = -3
        elif self.superBoostCoolDown>0:
            if self.kTime == 10: self.superBoostCoolDown-=1
            hud.getElementByTag("boostBar").colour = RED
            hud.getElementByTag("boostBar").updateSurface()
            
            self.dashInputBuffer -= 1 if self.dashInputBuffer > 0 else 0
            
            if inputs.inputEvent("Dash", False):
                self.dashInputBuffer = 10
            
        elif self.superBoostCoolDown<=-self.maxBoostCoolDown:
            hud.getElementByTag("boostBar").colour = ORANGE
            hud.getElementByTag("boostBar").updateSurface()

        elif self.superBoostCoolDown<=0:
            hud.getElementByTag("boostBar").colour = YELLOW
            hud.getElementByTag("boostBar").updateSurface()

        self.resetFrame = False


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
        self.bounce = False
        self.yVel = -self.jumpPower
        self.kTime=0
        self.jumpsLeft-=1
        self.wallJumpDelay = 20    
                
                
    def jump(self):
        level.levelPosy+=1
        if (self.touchGround or self.kTime>0):
            self.executeJump()
        elif self.homeTo == (0,0):
            if level.checkCollision(self.homingRange, False, [9]):
                self.xVel = 0
                self.yVel = 0
        level.levelPosy-=1

    def animate(self):
        returnImage = playerImages[0]
        walkAnimateFrame = int(self.walkAnimateFrame)
        if self.xVel == 0:
            returnImage = playerImages[0]

        elif abs(self.xVel) > 0 and self.touchGround or self.kTime>0:
            if walkAnimateFrame in [0, 2]:
                returnImage = playerImages[0]
            elif walkAnimateFrame == 1:
                returnImage = playerImages[1]
            else:
                returnImage = playerImages[2]

        if abs(self.xVel) > self.maxSpeed*2 and (self.touchGround or self.kTime>0):
            if walkAnimateFrame in [0, 2]:
                returnImage = playerImages[8]
            elif walkAnimateFrame == 1:
                returnImage = playerImages[9]
            else:
                returnImage = playerImages[10]

        if self.yVel > 2:
            returnImage = playerImages[3]

        if int(self.yVel) == 12:
            returnImage = playerImages[4]
        elif self.yVel > 12:
            returnImage = playerImages[5]
        elif self.yVel < 0 or self.homeTo != (0,0):
            if not self.bounce:
                self.jumpAnimateFrame += 0.25
                if self.jumpAnimateFrame == 8:
                    self.jumpAnimateFrame = 0
                if int(self.jumpAnimateFrame)%2 == 0:
                    returnImage = pygame.transform.rotate(playerImages[6], -90*int(self.jumpAnimateFrame/2))

                else:
                    returnImage = pygame.transform.rotate(playerImages[7], -90*(int((self.jumpAnimateFrame)-1)/2))
            else:
                self.jumpAnimateFrame += 0.25
                if self.jumpAnimateFrame >= 4:
                    self.jumpAnimateFrame = 0
                if self.jumpAnimateFrame >= 0:
                    returnImage = playerImages[14]
                if self.jumpAnimateFrame >= 1:
                    returnImage = playerImages[15]
                if self.jumpAnimateFrame >= 2:
                    returnImage = playerImages[16]
                if self.jumpAnimateFrame >= 3:
                    returnImage = playerImages[17]
            
                
        if self.climbedLastFrame: 
            self.climbedLastFrame=False
            if self.climbAnimateFrame >= 2: returnImage = playerImages[13]
            elif self.climbAnimateFrame >= 1: returnImage = playerImages[12]
            elif self.climbAnimateFrame >= 0: returnImage = playerImages[11]

        if not self.isRight:
            returnImage = pygame.transform.flip(returnImage, True, False)


        return returnImage

    def draw(self):
        #pygame.draw.rect(win, RED, self.charRect)
        #pygame.draw.rect(win, RED, self.homingRange)
        
        
        # Calculate the blit position
        blitPosX = 630 if (level.levelPosx > 635 and level.levelPosx - 635 + w < level.levelVis.get_width()) else (level.levelPosx-5 if level.levelPosx - 635 + w < level.levelVis.get_width() else w - (level.levelVis.get_width() - level.levelPosx)-5)
        blitPosY = 345 if level.levelPosy > 520 and level.levelPosy - 520 + h < level.levelVis.get_height() else (level.levelPosy - 175 if level.levelPosy - 520 + h < level.levelVis.get_height() else h - (level.levelVis.get_height() - level.levelPosy)-175)

        # Blit the animated character onto the screen
        win.blit(self.animate(), (blitPosX, blitPosY+1))
        if self.hat != "none":
            if self.isRight:
                win.blit(hats[self.hat], (blitPosX+13, blitPosY-9))
            else:
                win.blit(pygame.transform.flip(hats[self.hat], True, False), (blitPosX+1, blitPosY-9))


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
    def checkCollision(self, rectToCheck, tileToCheck=[0, 10, 15, 16, 17, 18], useTrim = True):
        global collisionTiles
        collided = False
        if useTrim:
            for tile in self.trimmedTiles:  
                collisionTiles += 1  
                if tile.tileID in tileToCheck:
                    tile.update()
                    if tile.checkCollision(rectToCheck):
                        collided = True
        else:#475, 300
            for tile in self.tiles:  
                if tile.tileID in tileToCheck:
                    if tile.rect.x > rectToCheck.x-75 and tile.rect.x < rectToCheck.x +75 and tile.rect.y > rectToCheck.y-100 and tile.rect.y < rectToCheck.y+100: 
                        tile.update()
                        if tile.checkCollision(rectToCheck):
                            collided = True
            
        return collided
    def trimTiles(self):
        self.trimmedTiles = []
        for tile in self.tiles:
            if tile.rect.x > 400 and tile.rect.x < 550 and tile.rect.y > 200 and tile.rect.y < 400: 
                self.trimmedTiles.append(tile)
    def update(self):
        for tile in self.tiles:
            tile.update()
        for entity in self.entities:
            entity.update()
    def drawEntities(self):
        for entity in self.entities:
            entity.draw(win, debug > 2)
    def singleUpdate(self):
        for tile in self.tiles:
            tile.singleUpdate()
    def posToString(self) -> str:
            return f"{self.x}-{self.y}"
    
    def reset(self):
        for entity in self.entities:
            entity.reset()
        
                        

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
        
        uiResults.getElementByTag("rank").changeImages([uiAnimations["rankings"][rank]])
        
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
        for chunk in self.activeChunks:
            chunk.singleUpdate()
    
    def checkCollision(self, rectToCheck, useTrim=True, tileToCheck=[0, 10, 15, 16, 17, 18, 27, 28]):
        global collisionTiles
        collided = False
        collisionTiles = 0
        
        for chunk in self.activeChunks:
            collided = chunk.checkCollision(rectToCheck, tileToCheck, useTrim)
            
            if collided:
                return collided
        
        return collided
    
    def loadBG(self, bgName):
        self.bg = pygame.image.load(f"backgrounds/{bgName}/bg.png").convert()
        
        paraLayer1 = pygame.image.load(f"backgrounds/{bgName}/layer1.png").convert_alpha()
        paraLayer2 = pygame.image.load(f"backgrounds/{bgName}/layer2.png").convert_alpha()
        
        
        self.paraLayer1 = pygame.Surface((w*2,h), pygame.SRCALPHA)
        self.paraLayer1.blit(paraLayer1, (0,0))
        self.paraLayer1.blit(paraLayer1, (w,0))
        
        self.paraLayer2 = pygame.Surface((w*2,h), pygame.SRCALPHA)
        self.paraLayer2.blit(paraLayer2, (0,0))
        self.paraLayer2.blit(paraLayer2, (w,0))

    @profile
    def changeLevel(self, resetPlayerPos=True, reloadLevel=False):
        self.first = True
        groundTiles = ["0"]
        pygame.mixer.Channel(7).fadeout(500)
        self.toggleBlockState = True
        
        win.fill(BLACK)
        win.blit(loadingFactFont.render(random.choice(facts), True, WHITE), (0,600))
        
        win.blit(bigFont.render("Reading level data...", True, WHITE), (0,90))
        
        window.blit(win, (0,0))
        pygame.display.flip()
        
        
        self.chunks = {}
        self.activeChunks = []
        
        #self.quickDraw = True
        if self.worldXLast != worldX or reloadLevel:
            self.worldXLast, self.worldYLast = worldX, worldY
            self.levels = []
            
            self.levelInfo = parseJsonFile(f"levels/levelInfo/{worldX}-{worldY}.json")
            
            
            levelJson = parseJsonFile(f"levels/levels/{worldX}-{worldY}.json")
            
            
            
            resliceImages(self.levelInfo["tileMapType"])
            
            self.loadBG(self.levelInfo['bgType'])        
            
            self.lowestPoint = 0
            self.highestPoint = float('inf')
            
            
            levelMap = {}
            
            chunksTemp = []
            
            self.indexOffset = 0
            
            largestX = 0
            for layer in levelJson["layers"]:
                for chunk in layer["chunks"]:
                    chunkX = chunk["x"]
                    chunkY = chunk["y"]
                    if(not f"{chunkX}-{chunkY}" in self.chunks):
                        chunksTemp.append(LevelChunk(int(chunkX), int(chunkY)))
                    for y in range(16):
                        for x in range(16):
                            if chunk["data"][(y*16) + x] != 0:
                                newTile = createTile((chunkX + x)*tileSize, (chunkY + y)*tileSize, int(chunk["data"][(y*16) + x])-1, tileSize)
                                self.levels.append(newTile)
                                
                                
                                
                                
                                if (chunkX + x)  > largestX:
                                    largestX = (chunkX + x)
                                
                                #set vars needed for tiles
                                newTile.index = len(self.levels)
                                newTile.level = self
                                newTile.player = player
                                newTile.gameManager = gameManager
                                newTile.win = win
                                if layer["name"] == "Main":
                                    if (chunkY + y)*tileSize < self.highestPoint:
                                        self.highestPoint = (chunkY + y)*tileSize
                                    
                                    elif (chunkY+y)*tileSize > self.lowestPoint:
                                        self.lowestPoint = (chunkY+y)*tileSize
                                #(int(chunk["data"][(y*16) + x])-1) 
                                
            
            
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
            
            
            for layer in levelJson["layers"]:
                if layer["name"] == "Main":
                    self.lowestPoint = layer["height"]*tileSize
        

            
            
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
                            window.blit(win, (0,0))
                            pygame.display.update()
                            loadingText = f"{str(int((tilesLoaded/len(self.levels))*100))}%"
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                run = False
                                quit()
                        
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
                        tilesLoaded+=1
                    
            else:
                for tile in self.levels:
                    pass
                print("pretty sure this never runs")
                    

        else:
            for tile in self.levels:
                tile.reload()
            if resetPlayerPos:
                spawnPos = self.getSpawn()
                player.x, player.y = spawnPos[0], spawnPos[1]
                
        pygame.draw.rect(win, BLACK, pygame.Rect(0, 0, w, h/2))
        win.blit(bigFont.render("Almost Done...", True, WHITE), (0,90))
        window.blit(win, (0,0))
        pygame.display.update()
                
        for tile in self.levels:
            tile.start()
            tile.levelDraw()
        deletedTiles = 100
        # Collect tiles to be deleted in one pass and update indexes if needed
        deleted_tiles_list = []
        new_levels = []
        self.levels[:] = [tile for tile in self.levels if not tile.toBeDeleted]

        for tile in self.levels:
            tile.index -= self.indexOffset
            tile.checkDelete()
            
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
        for chunk in self.activeChunks:
            chunk.trimTiles()
            for tile in chunk.tiles:
                if 400 < tile.rect.x < 550 and 200 < tile.rect.y < 400:
                    self.onScreenLevel.append(tile)
                elif -tileSize < tile.rect.x < 980 and -tileSize < tile.rect.y < 620:
                    self.onScreenLevel.append(tile)
                    
    
    
    def getSpawn(self):
        for tilesLoaded, tile in enumerate(self.levels):
            if tile.tileID == 3:
                return (self.levels[tilesLoaded].x, self.levels[tilesLoaded].y+160)
        return (0,0)
    
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
            # Calculate layer positions
            layerOnePos = ((-self.camX / 4) % 1280) - 1280
            layerTwoPos = ((-self.camX / 2) % 1280) - 1280

            # Blit parallax layers
            win.blit(self.paraLayer1, (layerOnePos, 0))
            win.blit(self.paraLayer2, (layerTwoPos, 0))
        

    def draw(self):
        
        self.drawBG()

        # Create and blit sub-surfaces
        subsurfaceBG = self.levelBG.subsurface((self.camX, self.camY, w, h))
        subsurfaceInter = self.levelInteract.subsurface((self.camX, self.camY, w, h))
        if self.toggleBlockState:
            subsurfaceToggle = self.levelToggleON.subsurface((self.camX, self.camY, w, h))
        else:
            subsurfaceToggle = self.levelToggleOFF.subsurface((self.camX, self.camY, w, h))
        subsurface = self.levelVis.subsurface((self.camX, self.camY, w, h))

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
    def __init__(self, text, showTime = 60):
        self.text = text
        self.showTime = showTime
        self.bg = pygame.Surface((w, 26), pygame.SRCALPHA)
        self.bg.fill((255,255,255,200))
    
    def draw(self, y):
        win.blit(self.bg, (0, (y*26)))
        win.blit(smallFont.render(self.text, True, BLACK), (0, ((y*26)+3)))
        self.showTime-=1
        if self.showTime<=0:
            debugLog.remove(self)

from UI import *

class AudioPlayer:
    def __init__(self) -> None:
        self.music = MusicSource("first.mp3")
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




def getPercentage(num, full):
    return (num/full)*100
def getIntPercentage(num, full):
    return int((num/full)*100)
  
def redrawScreen():
    global win
    if s.settings["backgroundDetail"] == 0: win = pygame.Surface((w,h))
        
    if gameManager.inGame:
        level.draw()
        
        #spikes.draw() 

        # for tile in level.onScreenLevel:
        #     tile.draw()
        
        player.draw()
    
    else:
        level.levelPosx+=1
        level.drawBG(False)

    if(debug > 0):
        debugUi.getElementByTag("FPSText").updateText("FPS: " + str(int(clock.get_fps())))
        if(debug > 1):
            fullDebugUi.getElementByTag("x").updateText("X: " + str(level.levelPosx))
            fullDebugUi.getElementByTag("y").updateText("Y: " + str(level.levelPosy))
            fullDebugUi.getElementByTag("ctiles").updateText("Collision Tiles: " + str(collisionTiles))
            fullDebugUi.getElementByTag("stomp").updateText("Stomp: " + str(player.stomp))
            fullDebugUi.getElementByTag("dtime").updateText("DeltaTime: " + str(deltaTime))
            fullDebugUi.getElementByTag("tframes").updateText("Target Frames: " + str(targetFrames))
            fullDebugUi.getElementByTag("tiles").updateText("Tiles: " + str(len(level.levels)))
            
            fullDebugUi.update()
            fullDebugUi.draw(win)
        
        debugUi.draw(win)

    hud.getElementByTag("boostBar").updateSize(getIntPercentage(player.maxBoostCoolDown-player.superBoostCoolDown, player.maxBoostCoolDown), 20)
    hud.getElementByTag("boostBarCoins").updateSize(getIntPercentage(player.maxBoostCoolDown-player.superBoostCoolDownCoins, player.maxBoostCoolDown), 20)
    hud
    hud.draw(win)
    uiPause.draw(win)
    uiPauseButtons.draw(win)
    uiMainMenu.draw(win)
    uiLevelTitle.draw(win)
    uiResults.draw(win)
    if gameManager.settingsMenu:
        uiSettings.draw(win)
        uiMainMenuSettings.draw(win)
        uiPauseSettings.draw(win)
        uiMainMenuSettingsScroll.draw(win)
        uiControls.draw(win)
        uiControlsMainMenu.draw(win)
        uiControlsPause.draw(win)
        uiControlsXbox.draw(win)

    
    for y, log in enumerate(debugLog):
        log.draw(y)
    
    window.blit(win, (0,0))
    # win.blit(pygame.transform.scale(win, (w, h)), (0,0))    
    
    # testEntity.draw(win)
    
    pygame.display.flip()
    

gameManager = GameManager()
player = Player()
keys = pygame.key.get_pressed()
level = Level()
player.reset()
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
        self.posx = 0
        self.posy = 0
        self.worldX = 0
        self.worldY = 0
        self.clicked = [False, False, False]
        self.clickDown = [False, False, False]
        self.scrolly = 0
        
        self.heldEvents = []
        
        self.controlType = -1 # -1=unknown 0=key 1=controller
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
    def inputEvent(self, inputName:str, canHold=True) -> bool:
        inputted = False
        careForHold = (not inputName in self.heldEvents or canHold)
        if self.controlType == -1 or self.controlType == 0:
            if inputName in self.inputDict and careForHold:
                for keyEnum in self.inputDict[inputName]:
                    if keys[keyEnum]:
                        inputted = True
                        self.controlType = 0
                 
        if self.controlType == -1 or self.controlType == 1:   
            if joystick.get_init():
                if not inputted and inputName in self.controllerDict and careForHold:
                    for button in self.controllerDict[inputName]:
                        if joystick.get_button(button):
                            inputted = True
                            self.controlType = 1
                if not inputted and inputName in self.axisDict and careForHold:
                    for axis in self.axisDict[inputName]:
                        if joystick.get_axis(axis[0]) > axis[1][0] and joystick.get_axis(axis[0]) < axis[1][1]:
                            inputted = True
                            self.controlType = 1
                        
        if inputted and not canHold:
            self.heldEvents.append(inputName)
        return inputted
    def resetHeldInputs(self):
        heldEventAfter = []
        for event in self.heldEvents:
            if self.inputEvent(event, True):
                heldEventAfter.append(event)
        self.heldEvents = copy.copy(heldEventAfter)
        self.controlType = -1
    def rumble(self, lf, hf, dur):
        if joystick.get_init():
            joystick.rumble(lf, hf, dur)

inputs = InputSystem()

gameManager.input = inputs

inputs.setKey(pygame.K_SPACE, "Jump")
inputs.setButton(0, "Jump")

inputs.setKey(pygame.K_LEFT, "MoveLeft")
inputs.setKey(pygame.K_a, "MoveLeft")
inputs.setButton(13, "MoveLeft")
inputs.setAxis(0, (-2, -0.1), "MoveLeft")

inputs.setKey(pygame.K_RIGHT, "MoveRight")
inputs.setKey(pygame.K_d, "MoveRight")
inputs.setButton(14, "MoveRight")
inputs.setAxis(0, (0.1, 2), "MoveRight")

inputs.setButton(1, "Stomp")
inputs.setKey(pygame.K_DOWN, "Stomp")
inputs.setKey(pygame.K_s, "Stomp")

inputs.setKey(pygame.K_RCTRL, "Dash")
inputs.setButton(2, "Dash")

inputs.setKey(pygame.K_LSHIFT, "Boost") 
inputs.setAxis(5, (-0.5, 2), "Boost")

inputs.setKey(pygame.K_LCTRL, "Climb")
inputs.setAxis(4, (-0.5, 2), "Climb")

inputs.setAxis(1, (-2, -0.5), "ClimbUp")
inputs.setButton(11, "ClimbUp")
inputs.setKey(pygame.K_UP, "ClimbUp")
inputs.setKey(pygame.K_w, "ClimbUp")

inputs.setAxis(1, (0.5, 2), "ClimbDown")
inputs.setButton(12, "ClimbDown")
inputs.setKey(pygame.K_DOWN, "ClimbDown")

inputs.setButton(4, "Restart1")
inputs.setKey(pygame.K_TAB, "Restart1")
inputs.setButton(5, "Restart2")
inputs.setKey(pygame.K_RSHIFT, "Restart2")
inputs.setButton(9, "Restart1")
inputs.setKey(pygame.K_TAB, "Restart1")
inputs.setButton(10, "Restart2")
inputs.setKey(pygame.K_RSHIFT, "Restart2")

inputs.setButton(6, "Pause")
inputs.setKey(pygame.K_ESCAPE, "Pause")


inputs.setKey(pygame.K_F4, "frateup")
inputs.setKey(pygame.K_F5, "fratedown")

inputs.setKey(pygame.K_F2, "screenshot")

inputs.setKey(pygame.K_F9, "toggleBlocks")

stallFrames = 0
frameAdvance = False
slashHeld = False


debugUi = UICanvas()
debugUi.addElement(UIText((0,h-66), "FPSText", "FPS:", 20, (0,0,0), 0))
debugUi.getElementByTag("FPSText").setBG((255,255,255))


fullDebugUi = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
fullDebugUi.addElement(UIText((0,20), "x", "X:", 20, (0,0,0), 0))
fullDebugUi.getElementByTag("x").setBG((255,255,255))
fullDebugUi.addElement(UIText((0,40), "y", "Y:", 20, (0,0,0), 0))
fullDebugUi.getElementByTag("y").setBG((255,255,255))
fullDebugUi.addElement(UIText((0,60), "ctiles", "Collision Tiles:", 20, (0,0,0), 0))
fullDebugUi.getElementByTag("ctiles").setBG((255,255,255))
fullDebugUi.addElement(UIText((0,80), "stomp", "Stomp:", 20, (0,0,0), 0))
fullDebugUi.getElementByTag("stomp").setBG((255,255,255))
fullDebugUi.addElement(UIText((0,100), "dtime", "DeltaTime:", 20, (0,0,0), 0))
fullDebugUi.getElementByTag("dtime").setBG((255,255,255))
fullDebugUi.addElement(UIText((0,120), "speed", "Speed:", 20, (0,0,0), 0))
fullDebugUi.getElementByTag("speed").setBG((255,255,255))
fullDebugUi.addElement(UIText((0,160), "tframes", "Target Frames:", 20, (0,0,0), 0))
fullDebugUi.getElementByTag("tframes").setBG((255,255,255))
fullDebugUi.addElement(UIText((0,180), "tiles", "Tiles:", 20, (0,0,0), 0))
fullDebugUi.getElementByTag("tiles").setBG((255,255,255))

fullDebugUi.addElement(UIButton((100, 350), "fly mode", gameManager.toggleFlyMode, "FLY MODE", 30, 20, (0,0,0), (RED, GREEN, BLUE)))


hud = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
hud.show = False
hud.addElement(UIRect((0, h-20), "fullBoostBar", 200, 20, GREY))
hud.addElement(UIRect((0, h-20), "boostBar", 100, 20, YELLOW))
hud.addElement(UIRect((100, h-20), "boostBarCoins", 100, 20, ORANGE))
hud.addElement(UIText((589,26), "timer", "00:00.00", 35, (0,0,0), 0))
hud.getElementByTag("timer").setBG((255,255,255, 150))
hud.addElement(UIImage((84, 683), "fullBoost", [uiAnimations["HUD"]["fullBoost"]]))
hud.addElement(UIImage((184, 683), "secondFullBoost", [uiAnimations["HUD"]["fullBoost"]]))
hud
hud.addElement(UIText((0,h-43), "coins", "Coins: 0/20", 20, (0,0,0), 0))
hud.getElementByTag("coins").setBG((255,255,255))


uiPause = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiPause.show = False
uiPause.addElement(UIRect((0,0), "PauseBG", w, h, (100,100,100,100)))
uiPause.addElement(UIText((0,h-85), "PauseText", "PAUSE", 50, (0,0,0), 20))
uiPause.getElementByTag("PauseText").setBG((255,255,255))

uiPause.addElement(UIText((w-100,0), "WorldText", "0-0", 50, (0,0,0), 0))


uiPauseButtons = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiPauseButtons.show = False
uiPauseButtons.addElement(UIButton((175, h-70), "Settings Button", gameManager.openSettingsPause, "Settings", 30, 20, (0,0,0), (RED, GREEN, BLUE)))
uiPauseButtons.addElement(UIButton((314, h-70), "Feedback Button", gameManager.openFeedback, "Feedback", 30, 20, (0,0,0), (RED, GREEN, BLUE)))

uiPauseButtons.addElement(UILevelSelect((0, 0), "0-0", level, (0, 0),"Dash Tutorial", 30, 20, (0,0,0), (RED, GREEN, BLUE)))
uiPauseButtons.addElement(UILevelSelect((0, 75), "1-1", level, (1, 1),"First Level", 30, 20, (0,0,0), (RED, GREEN, BLUE)))
uiPauseButtons.addElement(UILevelSelect((0, 150), "1-2", level, (1, 2),"Second Level", 30, 20, (0,0,0), (RED, GREEN, BLUE)))


uiPauseSettings = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiPauseSettings.show = False
uiPauseSettings.addElement(UIButton((w-210, 350), "back", gameManager.closeSettingPause, "Save Settings", 30, 20, (0,0,0), (RED, GREEN, BLUE)))
uiPauseSettings.addElement(UIButton((w-210, 650), "controls", gameManager.showControlsPauseMenu, "Controls", 30, 20, (0,0,0), (RED, GREEN, BLUE)))


uiMainMenu = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiMainMenu.addElement(UIText((100,100), "TITLE", "Really Fast Rat", 60, GREY, 0))
uiMainMenu.addElement(UIText((100,200), "SUBTITLE", "INDEV VERSION - 0.0.3 - INDEV 2", 20, GREY, 0))
uiMainMenu.addElement(UIButton((100, 350), "Start Button", gameManager.toggleLevelSelect, "Start", 30, 20, (0,0,0), (RED, GREEN, BLUE)))
uiMainMenu.addElement(UIButton((100, 450), "Settings Button", gameManager.openSettingsMainMenu, "Settings", 30, 20, (0,0,0), (RED, GREEN, BLUE)))
uiMainMenu.addElement(UIButton((100, 550), "Feedback Button", gameManager.openFeedback, "Feedback", 30, 20, (0,0,0), (RED, GREEN, BLUE)))

#https://forms.gle/Uez6tRceadLUjGgXA

uiMainMenu.addElement(UIImage((w-140, h-50), "ruby logo", [logo[2]]))

uiSettings = UICanvas(True, inputs=inputs, audioPlayer=audioPlayer)
uiSettings.show = False
uiSettings.addElement(UIText((150, 10), "TITLE", "Really Fast Rat Settings", 30, GREY, 0))
uiSettings.addElement(UIButton((10, 60), "MusicUp", gameManager.increaseMusicVolume, "Increase Music Volume", 30, 20, (0,0,0), (RED, GREEN, BLUE)))
uiSettings.addElement(UIText((310,60), "musicVolume", f"{s.settings['musicVolume']}%", 30, GREY, 20))
uiSettings.addElement(UIButton((410, 60), "MusicDown", gameManager.decreaseMusicVolume, "Decrease Music Volume", 30, 20, (0,0,0), (RED, GREEN, BLUE)))

uiSettings.addElement(UIButton((10, 160), "bgToggle", gameManager.toggleBG, "Toggle Background Detail", 30, 20, (0,0,0), (RED, GREEN, BLUE)))
uiSettings.addElement(UIText((350,160), "bgDetail", f"{gameManager.bgDetailLevels[s.settings['backgroundDetail']]}", 30, GREY, 20))

 
uiSettings.addElement(UIImage((w-90,80), "ratBluePrints", uiAnimations["bluePrints"], 6, lockScroll=True))




uiMainMenuSettings = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiMainMenuSettings.show = False
uiMainMenuSettings.addElement(UIButton((w-210, 350), "back", gameManager.closeSettingMainMenu, "Save Settings", 30, 20, (0,0,0), (RED, GREEN, BLUE)))
uiMainMenuSettings.addElement(UIButton((w-210, 650), "controls", gameManager.showControlsMainMenu, "Controls", 30, 20, (0,0,0), (RED, GREEN, BLUE)))

uiMainMenuSettingsScroll = UICanvas(True, inputs=inputs, audioPlayer=audioPlayer)
uiMainMenuSettingsScroll.show = False
uiMainMenuSettingsScroll.addElement(UIImage((450,160), "bgDetailImg", [uiAnimations["bgDetail"][s.settings["backgroundDetail"]]], 6))


uiControls = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiControls.show = False
uiControls.addElement(UIButton((115, 0), "reload", reloadController, "Reload Controller", 30, 20, (0,0,0), (RED, GREEN, BLUE)))

uiControlsXbox = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiControlsXbox.show = False
uiControlsXbox.addElement(UIImage((0,0), "xbox", [uiAnimations["controlLayouts"]["xbox"]], 6))
uiControlsXbox.addElement(UIText((289, 69), "climb", "CLIMB (HOLD)", 30, GREY, 0))
uiControlsXbox.addElement(UIText((860, 69), "run", "RUN (HOLD)", 30, GREY, 0))
uiControlsXbox.addElement(UIText((220, 400), "move", "MOVE", 30, GREY, 0))
uiControlsXbox.addElement(UIText((940, 250), "dash", "DASH", 30, GREY, 0))
uiControlsXbox.addElement(UIText((1180, 250), "stomp", "STOMP", 30, GREY, 0))
uiControlsXbox.addElement(UIText((1065, 440), "jump", "JUMP", 30, GREY, 0))


uiControlsMainMenu = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiControlsMainMenu.show = False
uiControlsMainMenu.addElement(UIButton((w-210, 0), "back", gameManager.hideControlsMainMenu, "Back", 30, 20, (0,0,0), (RED, GREEN, BLUE)))

uiControlsPause = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiControlsPause.show = False
uiControlsPause.addElement(UIButton((w-210, 0), "back", gameManager.hideControlsPauseMenu, "Back", 30, 20, (0,0,0), (RED, GREEN, BLUE)))


uiLevelTitle = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiLevelTitle.show = False
uiLevelTitle.addElement(UIImage((-562, 125), "bg", [uiAnimations["levelName"]["bg"]], 1))
uiLevelTitle.addElement(UIText((100, h+400), "lvlName", "LEVEL NAME", 40, BLACK))


uiResults = UICanvas(inputs=inputs, audioPlayer=audioPlayer)
uiResults.show = False
uiResults.addElement(UIRect((0,0), "resultBG", w, h, (100,100,100,100)))
uiResults.addElement(UIText((0,0), "ResultText", "RESULTS:", 50, (0,0,0), 20))
uiResults.getElementByTag("ResultText").setBG((255,255,255))

uiResults.addElement(UIRect((w-400,0), "timesBG", 400, 277, (100,100,100,100)))

uiResults.addElement(UIText((w-400,0), "s", "S RANK: 00:00", 30, (0,0,0), 20))
uiResults.addElement(UIText((w-400,50), "a", "A RANK: 00:00", 30, (0,0,0), 20))
uiResults.addElement(UIText((w-400,100), "b", "B RANK: 00:00", 30, (0,0,0), 20))
uiResults.addElement(UIText((w-400,150), "c", "C RANK: 00:00", 30, (0,0,0), 20))
uiResults.addElement(UIText((w-400,200), "d", "D RANK: 00:00", 30, (0,0,0), 20))

uiResults.addElement(UIImage((w-400, 338), "rank", [uiAnimations["rankings"]["s"]], 1))

uiResults.addElement(UIButton((w-600, 550), "continue", gameManager.nextLevel, "Continue", 30, 20, (0,0,0), (RED, GREEN, BLUE)))
uiResults.addElement(UIButton((w-600, 650), "try again", gameManager.closeResults, "Try Again", 30, 20, (0,0,0), (RED, GREEN, BLUE)))

uiResults.addElement(UIText((429,300), "timer", "00:00.00", 60, (0,0,0), 0))
uiResults.getElementByTag("timer").setBG((255,255,255, 150))

debug = 1
debugHeld = False

targetFrames = 60

titleLerpStall = 180
titleLerpStage = 0

#@profile
def main():
    # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    global posx, posy, clicked, pauseHeld, scrolly, keys, debugHeld, targetFrames, frameAdvance, stompHeld, spaceHeld, titleLerpStall, titleLerpStage, debug, slashHeld, stallFrames, deltaTime, worldX, worldY, run, useFullScreen
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
    
    for clickState in range(len(inputs.clickDown)):
        if inputs.clickDown[clickState]:
            inputs.clickDown[clickState] = clicked[clickState]
                
    inputs.resetHeldInputs()
    inputs.scrolly = scrolly
    
    #mouse getters
    clicked = pygame.mouse.get_pressed(num_buttons=3)
    posx, posy = pygame.mouse.get_pos()
    inputs.posx, inputs.posy = posx, posy
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
            player.process()
            if inputs.inputEvent("Jump") and not spaceHeld:
                player.jump()
                spaceHeld = True
            
            player.jumpPower = 11

            if (inputs.inputEvent("MoveLeft") and not inputs.inputEvent("MoveRight")) or (inputs.inputEvent("MoveRight") and not inputs.inputEvent("MoveLeft")):
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
            
            if inputs.inputEvent("Restart1") and inputs.inputEvent("Restart2"):
                player.lastSpawn = gameManager.ogSpawn
                level.reloadTiles()
                player.reset(True)


        if keys[pygame.K_r]:
            if keys[pygame.K_LCTRL]:
                if keys[pygame.K_LSHIFT]:
                    level.changeLevel(True, True)
                    debugLog.append(DebugLogText("Full Reload"))
                    player.reset(False)
                    playerImages = reloadPlayerImages()
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
    
    elif gameManager.settingsMenu:
        
        uiSettings.update()
        
        uiMainMenuSettings.update()
        
        uiPauseSettings.update()
        
        uiMainMenuSettingsScroll.update()
        
        uiControlsMainMenu.update()
        
        uiControlsPause.update()
        
        uiControls.update()
        
    elif gameManager.pause:
        
        uiPause.update()
        
        uiPauseButtons.update()
        
        if keys[pygame.K_r]:
            reloadController()
        
    if inputs.inputEvent("Pause") and not pauseHeld and gameManager.inGame:
        gameManager.togglePause()
        pauseHeld = True
        if gameManager.pause:
            pygame.mixer.Channel(7).pause()
        else:
            pygame.mixer.Channel(7).unpause()
            
    
    if debugHeld:
        debugHeld = keys[pygame.K_F3] or keys[pygame.K_F11]
    if keys[pygame.K_F3] and not debugHeld:
        debug += 1
        debugHeld = True
        if debug == 4:
            debug = 0
            
    if keys[pygame.K_F11] and not debugHeld:
        debugHeld = True
        useFullScreen = not useFullScreen
        # Set up the display
        if useFullScreen:
            window = pygame.display.set_mode((w, h), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF | pygame.HWSURFACE)
        else:
            window = pygame.display.set_mode((w, h), pygame.RESIZABLE | pygame.SCALED | pygame.DOUBLEBUF | pygame.HWSURFACE)

    
    if inputs.inputEvent("frateup", False):
        targetFrames+=10
    elif inputs.inputEvent("fratedown", False):
        targetFrames-=10
        if targetFrames <= 0: targetFrames = 10
    
    # Set the framerate
    deltaTime = clock.tick(targetFrames)* 0.001 * 60
    deltaTime = 1
    if deltaTime >= 5: deltaTime = 5

    
    
    if (keys[pygame.K_BACKSLASH] and not slashHeld) or frameAdvance:
        slashHeld = True
        waiting = True
        while waiting:
            deltaTime = 1
            redrawScreen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    quit()
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
        debugLog.append(DebugLogText(f"Game Screenshotted -> {screenshotName}", 100))
        
        
run = True
# Main game loop
while run:
    drawOnThread = s.settings["drawOnThread"]
    if drawOnThread:
        threading.Thread(target=redrawScreen, daemon=True).start()
    main()
    if not drawOnThread:
        redrawScreen()
        
    
pygame.quit()