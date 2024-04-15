import pygame, random, os, csv, copy
import math as maths

from resources import * #load all images from the external python file

from tiles import *
from colours import *


from jsonParse import *
from sign import *

os.system("cls")

random.seed(100)

useFullScreen = False # change to load on fullscreen or not

# Set win dimensions
w = 960
h = 600


tileSize = 20  

borderW = 50



# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

class noJoystick:
    def get_init(self):
        return False
    def get_button(self, num):
        return False
    def get_axis(self, num):
        return False
    def get_hat(self, num):
        return (0,0)

num_joysticks = pygame.joystick.get_count()

if num_joysticks > 0:
    if num_joysticks == 1:
        joystick = pygame.joystick.Joystick(0)
        joystick.rumble(1, 1, 1000)
    else:
        from extraControllers import getController
        joystick = pygame.joystick.Joystick(getController(num_joysticks, pygame.joystick))
        joystick.rumble(1, 1, 1000)
    joystick.init()
else:
    print("No controllers found.")
    joystick = noJoystick()

isXboxController = False
if joystick.get_init():
    if "xbox" in joystick.get_name().lower():
        isXboxController = True


# Set up the display
if useFullScreen:
    window = pygame.display.set_mode((w, h), pygame.FULLSCREEN | pygame.SCALED)
else:
    window = pygame.display.set_mode((w, h), pygame.RESIZABLE | pygame.SCALED)

    
win = pygame.Surface((w, h))
pygame.display.set_caption("Really Fast Rat")
pygame.display.set_icon(pygame.image.load('icon.png'))

logo=[pygame.image.load('logo/logosubless.png'), pygame.image.load('logo/logoSUB.png'), pygame.image.load('logo/logoBGless.png')]

# for i in range(500):
#     win.fill(LOGORED)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             run = False
#             quit()
#         elif event.type == pygame.VIDEORESIZE:
#             # This event is triggered when the window is resized
#             w, h = event.w, event.h
#     if i<=100:
#         win.blit(logo[0], (int(960/2)-168, int(600/2)-48))
        
#     elif i<200:
#         subLength = int(960/2)-168+40
#         subHeight = int(600/2)-40
#         win.blit(logo[0], (int(960/2)-168, int(600/2)-48))
#         win.blit(logo[1], (subLength, (subHeight*i / 100)-subHeight))
#     elif i<500:
#         win.blit(logo[0], (int(960/2)-168, int(600/2)-48))
#         win.blit(logo[1], (subLength, (subHeight*200 / 100)-subHeight))
    
#     window.blit(pygame.transform.scale(win, (w, h)), (0,0)) 
#     pygame.display.flip()



loadingTexts = ["LOADING IMAGES", "LOADING UI", "LOADING SOUNDS"]


# Set up fonts
smallFont = pygame.font.SysFont("arial", 20)
smallerFont = pygame.font.SysFont("arial", 15)
bigFont = pygame.font.SysFont("arial", 45)

# Set up timer
clock = pygame.time.Clock()

#load image text
win.blit(smallFont.render(loadingTexts[0], True, (255, 255, 255)), (0,200+(0*20)))
pygame.display.flip()





def resliceImages(tileType:str):
    tileImages.groundImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/ground.png"), tileSize, tileSize)
    tileImages.spikeImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/spikeTiles.png"), tileSize, tileSize)
    tileImages.bridgeImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/bridgeTiles.png"), tileSize, tileSize)
    tileImages.objectImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/objectTiles.png"), tileSize, tileSize)
    tileImages.groundBImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/groundB.png"), tileSize, tileSize)
    tileImages.groundCImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/groundC.png"), tileSize, tileSize)
    tileImages.groundDImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/groundD.png"), tileSize, tileSize)

    tileImages.backGroundAImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/backGroundA.png"), tileSize, tileSize)
    tileImages.backGroundBImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/backGroundB.png"), tileSize, tileSize)
    tileImages.backGroundCImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/backGroundC.png"), tileSize, tileSize)
    tileImages.backGroundDImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/backGroundD.png"), tileSize, tileSize)
    
    tileImages.movingPlatformImages = sliceTilemap(pygame.image.load(f"tilemap/{tileType}/movingPlatform.png"), tileSize, tileSize)


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

worldX, worldY = 1, 1


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
    def reset(self):
        self.speed = 3
        self.collectables = 0
        self.rareCollectables = 0
        self.pause = False
    def togglePause(self):
        self.pause = not self.pause
        uiPause.show = self.pause
        ui.show = not self.pause
        if self.pause:
            uiPause.getElementByTag("WorldText").updateText(f"{worldX} - {worldY}")
    def toggleMainMenu(self):
        self.mainMenu = not self.mainMenu
        uiMainMenu.show = self.mainMenu
    def toggleLevelSelect(self):
        self.toggleMainMenu()
        self.inGame = True
        ui.show = True
        level.changeLevel()


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
        self.teminalVelocity = 17
        self.boostDirection = 0
        self.canBoost = True
        self.decelSpeed = 0.2
        self.bonusXVel = 0
        self.superBoost = 5
        self.superBoostCoolDown = 0
        self.dashInputBuffer = 0

        self.jumpsLeft = 2

        self.stomp = False

        self.conveyorBonus = 0

        self.jumpPower = 11

        self.walkAnimateFrame = 0
        self.jumpAnimateFrame = 0
        self.isRight = True

        self.homingRange = pygame.Rect(self.charRect.x-240, self.charRect.y-240, 490, 500)
        self.canHomingAttck = True

        self.homeTo = (0,0)
        self.homeRight = False
        self.homeDown = False
        self.homeSpeed = 3
        self.homingCoolDown = 0

        self.powerUps = []
        
        self.lastSpawn = (0,0)
        
        self.wallJumpDelay = 0
    def reset(self, resetPlayerPos=True):
        gameManager.reset()
        self.xVel = 0
        self.yVel = 0
        self.homeTo = (0,0)
        level.levelPosx, level.levelPosy = self.lastSpawn[0], self.lastSpawn[1] 
        self.x, self.y = self.lastSpawn[0], self.lastSpawn[1] 
        self.kTime = 0      
        self.powerUps = []   
        self.superBoostCoolDown=0             
    def changeX(self, speed): 
        #self.x+=speed
        
        walled = False
        
        for i in range(abs(int(speed))):
            self.x += sign(int(speed))
            
            level.levelPosx = self.x
            
            for tile in level.trimmedLevel:
                tile.update()
            
            if level.checkCollision(self.charRect):
                self.wallCheck()
                walled = True
                break
        
        
        # for i in range(int(abs(speed))):
        #     self.x+=sign(speed)
        #     if level.checkCollision(self.charRect, True):
        #         canMoveUp = False
                
        #         for i in range(8):
        #             if not level.checkCollision(self.charRect, True) and not canMoveUp:
        #                 canMoveUp = True
        #             elif not canMoveUp:
        #                 level.levelPosy-=1
        #         if not canMoveUp:
        #             level.levelPosy+=8
        #             self.x-=sign(speed)
        #             self.xVel = 0
        
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
    def changeXVel(self, speed, isRight):
        
        
        self.wallJumped = False
        
        self.isRight = isRight
        if isRight:
            self.xVel += speed
            if self.xVel > self.maxSpeed and not (inputs.inputEvent("Boost") or self.homeTo!=(0,0)):
                self.xVel -= speed
                if self.xVel > self.maxSpeed:
                    self.xVel-=self.decelSpeed
            elif self.xVel > self.maxBoost and (inputs.inputEvent("Boost") or self.homeTo!=(0,0)):
                self.xVel = self.maxBoost
                if not self.canBoost:
                    self.xVel -= speed
                    if self.xVel > self.maxSpeed:
                        self.xVel-=self.decelSpeed
            for i in range(int(self.xVel)):
                self.x+=1
                
                level.levelPosx, level.levelPosy = self.x, self.y
        elif not isRight:
            self.xVel -= speed
            if self.xVel < -self.maxSpeed and not (inputs.inputEvent("Boost") or self.homeTo!=(0,0)):
                self.xVel += speed
                if self.xVel < -self.maxSpeed:
                    self.xVel+=self.decelSpeed
            elif self.xVel < -self.maxBoost and (inputs.inputEvent("Boost") or self.homeTo!=(0,0)):
                self.xVel = -self.maxBoost
                if not self.canBoost:
                    self.xVel += speed
                    if self.xVel < -self.maxSpeed:
                        self.xVel+=self.decelSpeed
            for i in range(-int(self.xVel)):
                self.x-=1
        self.xVel = round(self.xVel,2)
        if str(abs(self.xVel))[:3] == "0.1" or str(abs(self.xVel))[:3] == "0.0":
            self.xVel = 0

        if self.stomp:
            self.xVel = 0

        # if abs(self.xVel) > 19:
        #     self.xVel = 19*self.getDirNum()

        self.changeX(self.xVel)
        
        
        
    def wallCheck(self):
        self.climbedLastFrame=False
        velSign = sign(self.xVel)
        
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
                self.x-= 0.1*velSign
                level.levelPosx = self.x
                
            if (inputs.inputEvent("Jump", False)) and self.wallJumpDelay == 0:
                self.wallJumped = True
                self.yVel = -10
                self.xVel = 10*-velSign
            
            elif (inputs.inputEvent("Climb")):
                self.yVel = 0
                self.climbedLastFrame=True

                if inputs.inputEvent("ClimbUp"):
                    self.yVel = -3
                    level.levelPosy -= 30
                    level.levelPosx += velSign
                    if not level.checkCollision(self.charRect):
                        self.yVel = -7
                    level.levelPosy += 30
                    level.levelPosx -= velSign
                if inputs.inputEvent("ClimbDown"):
                    self.yVel = 3
                    
        



    def gravity(self):
        if self.homeTo != (0,0):
            self.homingCoolDown-=1
            if self.homingCoolDown==0:
                self.homeTo=(0,0)
        level.levelPosy = round(level.levelPosy, 2)
        if level.levelPosy > level.lowestPoint:
            self.die()
            
        for i in range(int(self.yVel)):
            self.y+=1
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
            self.y-=1
            level.levelPosx, level.levelPosy = self.x, self.y
            self.checkCeiling()
            
        if not level.checkCollision(self.charRect):
            self.yVel+=0.5
            if self.yVel > self.teminalVelocity:
                self.yVel = self.teminalVelocity
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
                    toochSemi = self.semied
                    self.semied = True
                    while not toochSemi:
                        level.levelPosy+=1
                        toochSemi = semiLevel.checkCollision(self.charRect)
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



        level.checkCollision(self.charRect, True, [2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14])




    def checkCeiling(self):
        level.levelPosy = self.y-1
        self.charRect.height = 1
        if level.checkCollision(self.charRect):
            self.yVel=+1
            self.y+=1
            level.levelPosy = self.y 
            self.touchGround=False
            self.kTime = 0
            self.charRect.height = 30
            return True
        else:
            self.charRect.height = 30
            return False

    def die(self):
        self.reset()

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
            self.teminalVelocity = 25
        else:
            self.teminalVelocity = 17

        self.gravity()
        if self.homeTo != (0,0):
            self.homingTo()

        if (inputs.inputEvent("Dash", False) or self.dashInputBuffer > 0) and self.superBoostCoolDown <= 0:
            self.maxBoost = (gameManager.speed*3)+ self.superBoost
            self.xVel += self.superBoost*self.getDirNum()
            inputs.rumble(0.1, abs(self.xVel/10)+0.3, 100)
            self.superBoostCoolDown = 60
            self.homeTo = (0,0)
            self.stomp = False
            if self.yVel > -3:
                self.yVel = -3
        elif self.superBoostCoolDown>0:
            self.superBoostCoolDown-=1
            ui.getElementByTag("boostBar").colour = RED
            ui.getElementByTag("boostBar").updateSurface()
            
            self.dashInputBuffer -= 1 if self.dashInputBuffer > 0 else 0
            
            if inputs.inputEvent("Dash", False):
                self.dashInputBuffer = 10
            
        elif self.superBoostCoolDown<=0:
            ui.getElementByTag("boostBar").colour = YELLOW
            ui.getElementByTag("boostBar").updateSurface()





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
        self.yVel = -self.jumpPower
        self.kTime=0
        self.jumpsLeft-=1
        self.wallJumpDelay = 20    
                
                
    def jump(self):
        level.levelPosy+=1
        if (self.touchGround or self.kTime>0) and self.jumpsLeft > 0:
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
            self.jumpAnimateFrame += 0.5
            if self.jumpAnimateFrame == 8:
                self.jumpAnimateFrame = 0
            if int(self.jumpAnimateFrame)%2 == 0:
                returnImage = pygame.transform.rotate(playerImages[6], -90*int(self.jumpAnimateFrame/2))

            else:
                returnImage = pygame.transform.rotate(playerImages[7], -90*(int((self.jumpAnimateFrame)-1)/2))

        if not self.isRight:
            returnImage = pygame.transform.flip(returnImage, True, False)


        return returnImage

    def draw(self):
        #pygame.draw.rect(win, RED, self.charRect)
        #pygame.draw.rect(win, RED, self.homingRange)
        
        
        # Calculate the blit position
        blitPosX = self.charRect.x - 5 if (level.levelPosx > 475 and level.levelPosx - 475 + w < level.levelVis.get_width()) else (level.levelPosx-5 if level.levelPosx - 475 + w < level.levelVis.get_width() else w - (level.levelVis.get_width() - level.levelPosx)-5)
        blitPosY = self.charRect.y if level.levelPosy > 475 and level.levelPosy - 475 + h < level.levelVis.get_height() else (level.levelPosy - 175 if level.levelPosy - 475 + h < level.levelVis.get_height() else h - (level.levelVis.get_height() - level.levelPosy)-175)

        # Blit the animated character onto the screen
        win.blit(self.animate(), (blitPosX, blitPosY))


        for y, powerUp in enumerate(self.powerUps):
            powerUp.draw(y)

        # if abs(self.xVel) >= self.maxBoost-1 and (self.touchGround or self.kTime>0):
        #     if not self.isRight:
        #         win.blit(pygame.transform.flip(random.choice(boostImages), True, False), (self.charRect.x-5, self.charRect.y))
        #     else:
        #         win.blit(random.choice(boostImages), (self.charRect.x-5, self.charRect.y))

   

class Level:
    def __init__(self):
        self.levelPosx = 0
        self.levelPosy = 0
        self.lowestPoint = 0
        self.worldXLast, self.worldYLast = -1, -1
        self.levelVis = pygame.Surface((0,0), pygame.SRCALPHA)
        self.quickDraw = keys[pygame.K_SPACE]
        self.offset = 1540
        self.switch = False

        self.levels=[]
        
        self.levelInfo = {}

    def updateTiles(self):
         for tile in self.trimmedLevel[::-1]:
            tile.update()
     
    def checkCollision(self, rectToCheck, useTrim=True, tileToCheck=[0, 10, 15, 16, 17, 18]):
        collided = False
        if useTrim:
            for tile in self.trimmedLevel[::-1]:
                if (tile.x < self.levelPosx+rectToCheck.width and tile.x > self.levelPosx-rectToCheck.width and tile.rect.y < player.charRect.y+300 and tile.rect.y > player.charRect.y-300) or tile.tileID == 18:
                    tile.update()
                    if tile.tileID in tileToCheck:
                        if tile.checkCollision(rectToCheck):
                            player.stomp = False
                            collided = True
        else:
            for tile in self.onScreenLevel[::-1]:
                if tile.x < self.levelPosx+rectToCheck.width and tile.x > self.levelPosx-rectToCheck.width and tile.rect.y < player.charRect.y+300 and tile.rect.y > player.charRect.y-300:
                    tile.update()
                    if tile.tileID in tileToCheck:
                        if tile.checkCollision(rectToCheck):
                            player.stomp = False
                            collided = True
        return collided
    def changeLevel(self, resetPlayerPos=True, reloadLevel=False):
        groundTiles = ["0"]
        if self.worldXLast != worldX or reloadLevel:
            self.worldXLast, self.worldYLast = worldX, worldY
            self.levels = []
            
            self.levelInfo = parseJsonFile(f"levels/levelInfo/{worldX}-{worldY}.json")
            
            
            
            resliceImages(self.levelInfo["tileMapType"])
            
            with open(f'levels/levels/{worldX}-{worldY}.csv', 'r') as csv_file:
                # Create a CSV reader object
                csv_reader = csv.reader(csv_file)
                tiles = list(csv_reader)

                # Loop through the rows in the CSV file
                for y, row in enumerate(tiles):
                    for x in range(len(row)):
                        if tiles[y][x] != "-1":
                            newTile = createTile(x*tileSize, y*tileSize, int(tiles[y][x]), tileSize)
                            self.levels.append(newTile)
                            
                            #set vars needed for tiles
                            newTile.level = self
                            newTile.player = player
                            newTile.gameManager = gameManager
                            newTile.win = win
                            
                            if y*tileSize+ (tileSize*11.5) > self.lowestPoint:
                                self.lowestPoint = y*tileSize+ (tileSize*11.5)
                                
            self.levelVis = pygame.Surface((len(tiles[0])*tileSize, (len(tiles)*tileSize)), pygame.SRCALPHA)
            self.levelVis.fill((0,0,0,0))
            
            self.levelBG = pygame.Surface((len(tiles[0])*tileSize, (len(tiles)*tileSize)), pygame.SRCALPHA)
            self.levelBG.fill((0,0,0,0))
            
            self.levelInteract = pygame.Surface((len(tiles[0])*tileSize, (len(tiles)*tileSize)), pygame.SRCALPHA)
            self.levelInteract.fill((0,0,0,0))
            
            #row = []
            
            tilesLoaded = 0
            if not self.quickDraw:
                loadingText = ""
                for tile in self.levels:
                    if tile.tileID == 3 and resetPlayerPos:
                        spawnPos = self.getSpawn()
                        gameManager.ogSpawn = spawnPos
                        self.levelPosx, self.levelPosy = spawnPos[0], spawnPos[1]
                        player.x, player.y = spawnPos[0], spawnPos[1]
                        #print(spawnPos[0], spawnPos[1])
                        player.lastSpawn = (self.levelPosx, self.levelPosy)
                    if tile.tileID != "-1":
                        if loadingText !=  f"{str(int((tilesLoaded/len(self.levels))*100))}%":
                            win.fill(BLACK)
                            win.blit(bigFont.render(f"Loading Level: {str(int((tilesLoaded/len(self.levels))*100))}%", True, WHITE), (0,90))
                            window.blit(win, (0,0))
                            pygame.display.flip()
                            loadingText = f"{str(int((tilesLoaded/len(self.levels))*100))}%"
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                run = False
                                quit()
                            elif event.type == pygame.VIDEORESIZE:
                                # This event is triggered when the window is resized
                                w, h = event.w, event.h
                        if tiles[int(tile.y/20)][int(tile.x/20)] == "0":
                            self.getTileImage(tile, tiles, "0", row, tilesLoaded, tileImages.groundImages)
                        if tiles[int(tile.y/20)][int(tile.x/20)] == "1":
                            self.getTileImage(tile, tiles, "1", row, tilesLoaded, tileImages.bridgeImages, ["0", "1", "15", "16", "17"])
                        if tiles[int(tile.y/20)][int(tile.x/20)] == "2":
                            self.getTileImage(tile, tiles, "2", row, tilesLoaded, tileImages.spikeImages, ["0", "2", "15", "16", "17"])
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "4":
                            tile.image = tileImages.objectImages[1]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "5":
                           tile.image = tileImages.objectImages[3]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "6":
                            tile.image = tileImages.objectImages[0]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "7":
                            tile.image = tileImages.objectImages[4]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "8":
                            tile.image = tileImages.objectImages[2]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "10":
                            tile.image = tileImages.objectImages[5]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "14":
                            tile.image = tileImages.objectImages[6]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "15":
                            self.getTileImage(tile, tiles, "15", row, tilesLoaded, tileImages.groundBImages)
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "16":
                            self.getTileImage(tile, tiles, "16", row, tilesLoaded, tileImages.groundCImages, ["16", "17"])
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "17":
                            self.getTileImage(tile, tiles, "17", row, tilesLoaded, tileImages.groundDImages, ["16", "17"])
                            
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "18":
                            self.getTileImage(tile, tiles, "18", row, tilesLoaded, tileImages.backGroundAImages, ["0", "15", "16", "17", "18", "19"])
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "19":
                            self.getTileImage(tile, tiles, "19", row, tilesLoaded, tileImages.backGroundBImages, ["0", "15", "16", "17", "18", "19"])
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "20":
                            self.getTileImage(tile, tiles, "20", row, tilesLoaded, tileImages.backGroundCImages, ["0", "15", "16", "17", "20", "21"])
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "21":
                            self.getTileImage(tile, tiles, "21", row, tilesLoaded, tileImages.backGroundDImages, ["0", "15", "16", "17", "20", "21"])
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "22":
                            self.getTileImage(tile, tiles, "22", row, tilesLoaded, tileImages.movingPlatformImages, ["22"])
                        tilesLoaded+=1
                    
            else:
                for tile in self.levels:
                    above, below, left, right = False, False, False, False
                    if tile.tileID == 0:# Check neighbors
                        if tile.y!=0:
                            if tiles[int(tile.y/tileSize)-1][int(tile.x/tileSize)] in groundTiles:
                                above = True
                        if tile.y/tileSize!=len(tiles)-1:
                            if tiles[int(tile.y/tileSize)+1][int(tile.x/tileSize)] in groundTiles:
                                below = True
                        if tile.x!=0:
                            if tiles[int(tile.y/tileSize)][int(tile.x/tileSize)-1] in groundTiles:
                                left = True
                        if tile.x/tileSize!=len(row)-1:
                            if tiles[int(tile.y/tileSize)][int(tile.x/tileSize)+1] in groundTiles:
                                right = True

                        if above and below and left and right:
                            tile.toBeDeleted = True

        else:
            for tile in self.levels:
                tile.reload()
            if resetPlayerPos:
                spawnPos = self.getSpawn()
                player.x, player.y = spawnPos[0], spawnPos[1]
                
                
        for tile in self.levels:
            tile.start()
        
        audioPlayer.playMusic(AudioSource(f"music/{self.levelInfo['music']}"))
                
        
    def getTileImage(self, tile, tiles, typeNum:str, row, tilesLoaded, tilesToBeUsed, groundTiles=["0", "15"]):
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

        # Check neighbors
        if tile.y!=0:
            if tiles[int(tile.y/tileSize)-1][int(tile.x/tileSize)] in groundTiles:
                above = True
        if tile.y/tileSize!=len(tiles)-1:
            if tiles[int(tile.y/tileSize)+1][int(tile.x/tileSize)] in groundTiles:
                below = True
        if tile.x!=0:
            if tiles[int(tile.y/tileSize)][int(tile.x/tileSize)-1] in groundTiles:
                left = True
        if tile.x/tileSize!=len(row)-1:
            if tiles[int(tile.y/tileSize)][int(tile.x/tileSize)+1] in groundTiles:
                right = True
        if tiles[int(tile.y/tileSize)][int(tile.x/tileSize)] == typeNum:
            # Get the corresponding image based on neighbor pattern
            neighbors = (above, below, left, right)
            self.levels[tilesLoaded].image = tilesToBeUsed[neighbor_image_map.get(neighbors, 6)]
            tile.image = tilesToBeUsed[neighbor_image_map.get(neighbors, 6)].convert_alpha()
            
            newImage = pygame.Surface((tileSize,tileSize), pygame.SRCALPHA)
            newImage.blit(tile.image, (0,0))


            

            
            #right side
            if tile.y!=0 and tile.x/tileSize!=len(row)-1 and above and right:
                if not tiles[int(tile.y/tileSize)-1][int(tile.x/tileSize)+1] in groundTiles:
                    newImage.blit(tilesToBeUsed[5], (0,0))
            if tile.y/tileSize!=len(tiles)-1 and tile.x/tileSize!=len(row)-1 and below and right:
                if not tiles[int(tile.y/tileSize)+1][int(tile.x/tileSize)+1] in groundTiles:
                    newImage.blit(pygame.transform.rotate(tilesToBeUsed[5], -90), (0,0))

            #left side
            if tile.y!=0 and tile.x!=0 and above and left:
                if not tiles[int(tile.y/tileSize)-1][int(tile.x/tileSize)-1] in groundTiles:
                    newImage.blit(pygame.transform.rotate(tilesToBeUsed[5], 90), (0,0))
            if tile.y/tileSize!=len(tiles)-1 and tile.x!=0 and below and left:
                if not tiles[int(tile.y/tileSize)+1][int(tile.x/tileSize)-1] in groundTiles:
                    newImage.blit(pygame.transform.rotate(tilesToBeUsed[5], 180), (0,0))

            
            tile.image = newImage
            #self.levelVis.blit(groundImages[neighbor_image_map.get(neighbors, 6)], (self.levels[tilesLoaded].x, self.levels[tilesLoaded].y))
            if neighbor_image_map.get(neighbors, 6) == 10:
                tile.toBeDeleted = True

    def reloadTiles(self):
        for tile in self.levels:
            tile.reload()

    def trimLevel(self):
        self.trimmedLevel = []
        self.onScreenLevel = []
        for tile in self.levels:
            if tile.rect.x > 400 and tile.rect.x < 550 and tile.rect.y > 200 and tile.rect.y < 400:
                self.trimmedLevel.append(tile)
                self.onScreenLevel.append(tile)
            elif tile.rect.x > -tileSize and tile.rect.x < 980 and tile.rect.y > -tileSize and tile.rect.y < 620:
                self.onScreenLevel.append(tile)
                if tile.tileID == 18:
                    self.trimmedLevel.append(tile)
    
    def getSpawn(self):
        for tilesLoaded, tile in enumerate(self.levels):
            if tile.tileID == 3:
                return (self.levels[tilesLoaded].x, self.levels[tilesLoaded].y+160)
        return (0,0)
    

    def draw(self):
        
        subPosX = (self.levelPosx - 475) if (self.levelPosx > 475 and self.levelPosx - 475 + w < self.levelVis.get_width()) else (0 if self.levelPosx - 475 + w < self.levelVis.get_width() else self.levelVis.get_width() - w)
        subPosY = (self.levelPosy - 475) if (self.levelPosy > 475 and self.levelPosy - 475 + h < self.levelVis.get_height()) else (0 if self.levelPosy - 475 + h < self.levelVis.get_height() else self.levelVis.get_height() - h)

        # Create the subsurface
        subsurfaceInter = pygame.Surface.subsurface(self.levelInteract, (subPosX, subPosY), (w, h))
        subsurface = pygame.Surface.subsurface(self.levelVis, (subPosX, subPosY), (w, h))
        subsurfaceBG = pygame.Surface.subsurface(self.levelBG, (subPosX, subPosY), (w, h))
        
        #draws subsurface of level
        win.blit(subsurfaceInter, (0, 0))
        win.blit(subsurfaceBG, (0, 0))
        win.blit(subsurface, (0, 0))
        
        # old level draw code
        # win.blit(self.levelVis, (-self.levelPosx+475,-self.levelPosy+475))
        
        
        
        # silly :3
        # self.levelVis.blit(logo[0], (self.levelPosx, self.levelPosy))
        
        
        #win.blit(pygame.Surface.subsurface(self.levelVis, (subPosX, self.levelVis.get_height()-h), (w, h)), (0,0))
        
        # full level view
        # win.blit(pygame.transform.scale(self.levelVis, (w,h)), (0,0))
       
        # save image of level (super duper laggy
        # pygame.image.save(self.levelVis, 'lvl.png')

class semiLevel:
    def __init__(self):
        pass
    def checkCollision(self, rectToCheck, tilesToCheck=[1, 22]):
        feetRect = pygame.Rect(475, player.charRect.y+29, 20, 1)
        collided = False
        if player.yVel >= 0:
            for tile in level.trimmedLevel:
                tile.update()
                if (tile.x < level.levelPosx+20 and tile.x > level.levelPosx-20 and tile.rect.y < player.charRect.y+50 and tile.rect.y > player.charRect.y-20) or tile.tileID == 22:
                    if tile.tileID in tilesToCheck and not collided:
                        if tile.checkCollisionRect(feetRect):
                            collided = True
                            break
        return collided and not inputs.inputEvent("Stomp")
    def draw(self):
        #win.blit(self.image, (-level.levelPosx+475,0))
        pass




class DebugLogText:
    def __init__(self, text, showTime = 60):
        self.text = text
        self.showTime = showTime
        self.bg = pygame.Surface((960, 26), pygame.SRCALPHA)
        self.bg.fill((255,255,255,200))
    
    def draw(self, y):
        win.blit(self.bg, (0, (y*26)))
        win.blit(smallFont.render(self.text, True, BLACK), (0, ((y*26)+3)))
        self.showTime-=1
        if self.showTime<=0:
            debugLog.remove(self)


class UICanvas:
    def __init__(self) -> None:
        self.UIComponents = []
        self.show = True
    def addElement(self, element):
        self.UIComponents.append(element)
    def getElementByTag(self, tag:str):
        for element in self.UIComponents:
            if element.tag == tag:
                return element
    def draw(self):
        if self.show:
            for element in self.UIComponents:
                element.draw()
    def update(self):
        for element in self.UIComponents:
            element.update()

class UIElement:
    def __init__(self, screenPos, tag:str, hasShadow=False, shadowOffset=0, shadowColour=(255,255,255)) -> None:
        self.screenPos = screenPos
        self.tag = tag
        self.surface = pygame.Surface((0,0), pygame.SRCALPHA)
        self.show = True
        self.hasShadow = hasShadow
        self.shadowOffset = shadowOffset
        self.shadowColour = shadowColour
    def toggleShow(self):
        self.show = not self.show
    def setShow(self, setTo:bool):
        self.show = setTo
    def moveTo(self, newPos):
        self.screenPos = newPos
    def draw(self, surf=win,padding=(0,0),screenPos=None, blitSurf=None, drawShadow=True):
        screenPosWasNone = screenPos==None
        if screenPos==None:
            screenPos = self.screenPos
        if blitSurf==None:
            blitSurf = self.surface
        if self.show:
            surf.blit(blitSurf, (int(screenPos[0]+padding[0]), screenPos[1]+padding[1]))
    def update(self):
        pass

class UIText(UIElement):
    def __init__(self, screenPos, tag:str, text="", fontSize=10, colour=(0,0,0), padding=20) -> None:
        super().__init__(screenPos, tag)
        self.text = text
        self.fontSize = fontSize
        self.colour = colour
        self.font = pygame.font.SysFont("arial", self.fontSize)
        self.padding = padding

        self.setBG(CLEAR)

        self.updateText(text)
    def updateText(self, newText:str, fontSize=None, colour=None):
        if fontSize!=None:
            self.fontSize = fontSize
        if colour!=None:
            self.colour = colour
        self.font = pygame.font.SysFont("arial", self.fontSize)
        textSurface = self.font.render(newText, True, self.colour)
        self.surface = pygame.Surface((textSurface.get_width()+ self.padding*2, textSurface.get_height()+ self.padding*2), pygame.SRCALPHA)
        self.surface.blit(textSurface, (self.padding, self.padding))

        if self.bg.tag!="textBGEmpty":
            self.bg.updateSize(self.surface.get_width(),self.surface.get_height())
            self.bg.updateSurface()

        self.surface.blit(self.bg.surface, (0,0))
        self.surface.blit(textSurface, (self.padding,self.padding))
    def setBG(self, colour):
        self.bg = UIRect((0,0), "textBG", self.surface.get_width(),self.surface.get_height(), colour)
        self.updateText(self.text)
    def removeBG(self):
        self.bg.tag = "textBGEmpty"
        self.updateText(self.text)
    def updatePadding(self, newPadding):
        self.padding = newPadding
        self.updateText(self.text)

class UIRect(UIElement):
    def __init__(self, screenPos, tag:str, w:int, h:int, colour=(0,0,0)) -> None:
        super().__init__(screenPos, tag)
        self.updateRect(w, h, colour)
    def updateRect(self, w:int, h:int, colour=None):
        self.w, self.h = w, h
        self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
        if colour != None:
            self.colour = colour
        self.surface.fill(colour)
    def updateSurface(self):
        self.surface.fill(self.colour)
    def updateSize(self, w, h):
        self.w, self.h = w, h
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
        self.surface.fill(self.colour)
    def updatePos(self, x,y):
        self.screenPos = (x,y)
        
class UIButton(UIText):
    def __init__(self, screenPos, tag:str, onClick, text="", fontSize=10, padding=20, textColour=(0, 0, 0), buttonColours=((255,255,255), (127,127,127), (0,0,0)), canHold=False) -> None:
        super().__init__(screenPos, tag, text, fontSize, textColour, padding)
        self.setBG(buttonColours[0])
        self.onClick = onClick
        self.held = False
        self.canHold = canHold
        self.buttonColours = buttonColours
    def update(self):
        tempRect = self.surface.get_rect()
        tempRect.x, tempRect.y = self.screenPos[0], self.screenPos[1]
        if tempRect.collidepoint(posx, posy):
            self.setBG(self.buttonColours[1])
            if clicked[0]:
                self.setBG(self.buttonColours[2])
                if not self.held:
                    self.held = not self.canHold
                    self.onClick()
        if not tempRect.collidepoint(posx, posy):
            self.setBG(self.buttonColours[0])

        self.held = clicked[0] or self.canHold



class AudioPlayer:
    def __init__(self) -> None:
        pass
    def playSound(self, soundSrc, volume=100, channel=0):
        sound = soundSrc.sound
        sound.set_volume(volume)
        if channel != 0 or channel > 6:
            pygame.mixer.Channel(channel).play(sound)
        else:
            sound.play()
    def playMusic(self, musicSrc, volume=100):
        sound = musicSrc.sound
        sound.set_volume(volume)
        pygame.mixer.Channel(7).play(sound, -1)
    
class AudioSource:
    def __init__(self, soundPath:str) -> None:
        self.sound = pygame.mixer.Sound("sound/" + soundPath)

audioPlayer = AudioPlayer()

jump = AudioSource("jump.mp3")
music = AudioSource("music/music.mp3")

# audioPlayer.playMusic(music)


def getPercentage(num, full):
    return (num/full)*100
def getIntPercentage(num, full):
    return int((num/full)*100)

        

def redrawScreen():
        
    win.fill(WHITE)
    if gameManager.inGame:
        level.draw()
        
        #spikes.draw() 

        for tile in level.onScreenLevel:
            tile.draw()
        
        player.draw()

    for y, log in enumerate(debugLog):
        log.draw(y)

    ui.getElementByTag("FPSText").updateText("FPS: " + str(int(clock.get_fps())))

    ui.getElementByTag("boostBar").updateSize(getIntPercentage(60-player.superBoostCoolDown, 60), 20)
    
    ui.draw()
    uiPause.draw()
    uiMainMenu.draw()

    window.blit(win, (0,0))    
    # window.blit(pygame.transform.scale(win, (w, h)), (0,0))    
    pygame.display.flip()

gameManager = GameManager()
player = Player()
keys = pygame.key.get_pressed()
level = Level()
player.reset()
semiLevel = semiLevel()

debugLog = []


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
        if inputName in self.inputDict and careForHold:
            for keyEnum in self.inputDict[inputName]:
                if keys[keyEnum]:
                    inputted = True
        if joystick.get_init():
            if not inputted and inputName in self.controllerDict and careForHold:
                for button in self.controllerDict[inputName]:
                    if joystick.get_button(button):
                        inputted = True
            if not inputted and inputName in self.axisDict and careForHold:
                for axis in self.axisDict[inputName]:
                    if joystick.get_axis(axis[0]) > axis[1][0] and joystick.get_axis(axis[0]) < axis[1][1]:
                        inputted = True
                        
        if inputted and not canHold:
            self.heldEvents.append(inputName)
        return inputted
    def resetHeldInputs(self):
        heldEventAfter = []
        for event in self.heldEvents:
            if self.inputEvent(event, True):
                heldEventAfter.append(event)
        self.heldEvents = copy.copy(heldEventAfter)
                
    def rumble(self, lf, hf, dur):
        if joystick.get_init():
            joystick.rumble(lf, hf, dur)

inputs = InputSystem()
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

# inputs.setButton(1, "Stomp")
# inputs.setKey(pygame.K_DOWN, "Stomp")
# inputs.setKey(pygame.K_s, "Stomp")

inputs.setKey(pygame.K_RCTRL, "Dash")
inputs.setButton(2, "Dash")

inputs.setKey(pygame.K_LSHIFT, "Boost") 
inputs.setAxis(5, (-0.5, 2), "Boost")

inputs.setKey(pygame.K_LCTRL, "Climb")
inputs.setAxis(4, (-0.5, 2), "Climb")

inputs.setAxis(1, (-2, -0.1), "ClimbUp")
inputs.setButton(11, "ClimbUp")
inputs.setKey(pygame.K_UP, "ClimbUp")

inputs.setAxis(1, (0.1, 2), "ClimbDown")
inputs.setButton(12, "ClimbDown")
inputs.setKey(pygame.K_DOWN, "ClimbDown")

inputs.setButton(4, "Restart1")
inputs.setKey(pygame.K_TAB, "Restart1")
inputs.setButton(15, "Restart2")
inputs.setKey(pygame.K_RSHIFT, "Restart2")

inputs.setButton(6, "Pause")
inputs.setKey(pygame.K_ESCAPE, "Pause")

stallFrames = 0
frameAdvance = False
slashHeld = False




ui = UICanvas()
ui.show = False
ui.addElement(UIText((0,0), "FPSText", "FPS:", 20, (0,0,0), 0))
ui.getElementByTag("FPSText").setBG((255,255,255))
ui.addElement(UIRect((0, 580), "boostBar", 100, 20, YELLOW))


uiPause = UICanvas()
uiPause.show = False
uiPause.addElement(UIRect((0,0), "PauseBG", w, h, (100,100,100,100)))
uiPause.addElement(UIText((0,0), "PauseText", "PAUSE", 50, (0,0,0), 0))
uiPause.getElementByTag("PauseText").setBG((255,255,255))

uiPause.addElement(UIText((w-100,0), "WorldText", "0-0", 50, (0,0,0), 0))



uiMainMenu = UICanvas()
uiMainMenu.addElement(UIText((100,100), "TITLE", "Really Fast Rat", 60, GREY, 0))
uiMainMenu.addElement(UIButton((860, 350), "Start Button", gameManager.toggleLevelSelect, "Start", 30, 20, (0,0,0), (RED, GREEN, BLUE)))


run = True
# Main game loop
while run:
    scrolly = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
        elif event.type == pygame.MOUSEWHEEL:
            scrolly = event.y
        elif event.type == pygame.VIDEORESIZE:
            # This event is triggered when the window is resized
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
    
    
    
    
    level.checkCollision(player.charRect, True, [18])
    
    
    keys = pygame.key.get_pressed()

    if pauseHeld:
        pauseHeld = inputs.inputEvent("Pause")

    if not gameManager.pause and gameManager.inGame:

        if stompHeld:
            stompHeld = inputs.inputEvent("Stomp")
        if spaceHeld:
            spaceHeld = inputs.inputEvent("Jump")

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
            
            
        
        if not player.climbedLastFrame and player.kTime < 8:
            if inputs.inputEvent("Stomp") and not stompHeld and not player.climbedLastFrame:
                player.stomp = True
                player.yVel = 20
                stompHeld = True


        if inputs.inputEvent("Restart1") and inputs.inputEvent("Restart2"):
            player.lastSpawn = gameManager.ogSpawn
            level.reloadTiles()
            player.die()

        if keys[pygame.K_r]:
            if keys[pygame.K_LCTRL]:
                if keys[pygame.K_LSHIFT]:
                    level.changeLevel(True, True)
                    debugLog.append(DebugLogText("Full Reload"))
                    player.reset(False)
                elif keys[pygame.K_LALT]:
                    debugLog.append(DebugLogText("QuickDraw Load"))
                    level.quickDraw = True
                    level.changeLevel(True, True)
                    player.reset()
                else:
                    debugLog.append(DebugLogText("Advanced Reload"))
                    level.changeLevel(False, True)
                    player.reset(False)
            elif keys[pygame.K_p]:
                debugLog.append(DebugLogText("Player Reload"))
                level.changeLevel(True, False)
                player.reset()
            else:
                debugLog.append(DebugLogText("Basic Reload"))
                level.changeLevel(False)
        
        if keys[pygame.K_t] and keys[pygame.K_LCTRL]:
                level.quickDraw = False
                level.changeLevel(True, True)

        
        
        gameManager.speed = 3
        
        for tile in level.levels:
            tile.update()
            
        for tile in level.levels:
            tile.singleUpdate()
    
    elif gameManager.mainMenu:
        
        uiMainMenu.update()
        
    if inputs.inputEvent("Pause") and not pauseHeld:
        gameManager.togglePause()
        pauseHeld = True
        
    

    #redraw win
    redrawScreen()
    # Set the framerate
    deltaTime = clock.tick(60)/10

    
    
    if (keys[pygame.K_BACKSLASH] and not slashHeld) or frameAdvance:
        slashHeld = True
        waiting = True
        while waiting:
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