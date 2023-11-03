import pygame, random, asyncio, os, csv
import math as maths

os.system("cls")


# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
GREY = (128, 128, 128)
WHITE = (255,255,255)
LOGORED = (170, 32, 32)
CYAN = (0, 159, 159)
GOLD = (255, 215, 0)
MAGENTA = (255, 0, 255)
LIME = (181, 255, 81)

TEAL = (0, 128, 128)
SILVER = (192, 192, 192)

# Set win dimensions
w = 960
h = 600
borderW = 50



# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the display
window = pygame.display.set_mode((w, h), pygame.RESIZABLE)
win = pygame.Surface((w, h))
pygame.display.set_caption("Really Fast Rat")
pygame.display.set_icon(pygame.image.load('icon.png'))

logo=[pygame.image.load('logo/logosubless.png'), pygame.image.load('logo/logoSUB.png'), pygame.image.load('logo/logoBGless.png')]

for i in range(500):
    win.fill(LOGORED)
    if i<=100:
        win.blit(logo[0], (int(960/2)-168, int(600/2)-48))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()
            elif event.type == pygame.VIDEORESIZE:
                # This event is triggered when the window is resized
                w, h = event.w, event.h
    elif i<200:
        subLength = int(960/2)-168+40
        subHeight = int(600/2)-40
        win.blit(logo[0], (int(960/2)-168, int(600/2)-48))
        win.blit(logo[1], (subLength, (subHeight*i / 100)-subHeight))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()
            elif event.type == pygame.VIDEORESIZE:
                # This event is triggered when the window is resized
                w, h = event.w, event.h
    elif i<500:
        win.blit(logo[0], (int(960/2)-168, int(600/2)-48))
        win.blit(logo[1], (subLength, (subHeight*200 / 100)-subHeight))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()
            elif event.type == pygame.VIDEORESIZE:
                # This event is triggered when the window is resized
                w, h = event.w, event.h
    
    window.blit(pygame.transform.scale(win, (w, h)), (0,0)) 
    pygame.display.flip()



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

#LOAD IMAGES 
playerImages = [
    pygame.image.load("player/player.png"),
    pygame.image.load("player/walk1.png"),
    pygame.image.load("player/walk2.png"),
    pygame.image.load("player/fall0.png"),
    pygame.image.load("player/fall1.png"),
    pygame.image.load("player/fall2.png"),
    pygame.image.load("player/jump1.png"),
    pygame.image.load("player/jump2.png"),
    pygame.image.load("player/run0.png"),
    pygame.image.load("player/run1.png"),
    pygame.image.load("player/run2.png")
]
boostImages = [
    pygame.image.load("player/boost0.png"),
    pygame.image.load("player/boost1.png"),
    pygame.image.load("player/boost2.png")
]
tile_width = 20
tile_height = 20  # Replace with your tile height

tileSheet = pygame.image.load("tilemap/sampleTiles.png")

tileImages = []  # This list will hold your individual tiles

for y in range(0, tileSheet.get_height(), tile_height):
    for x in range(0, tileSheet.get_width(), tile_width):
        tile = tileSheet.subsurface(pygame.Rect(x, y, tile_width, tile_height))
        tileImages.append(tile)



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

worldX, worldY = 1, 0   

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
    def reset(self):
        self.speed = 3
        self.collectables = 0
        self.rareCollectables = 0

class PowerUp:
    def __init__(self, powerType, time = 120):
        self.type = powerType
        self.time = time
    def draw(self, y):
        win.blit(smallFont.render(f"powerup: {int(self.time/60)}", True, RED), (850, (y*20)))
        player.jumpPower += 6
        self.time-=1
        if self.time <=0:
            player.powerUps.remove(self)

class Player:
    def __init__(self):
        self.semied = False
        self.x = 475
        self.y = 0
        self.xVel = 0
        self.yVel = 0
        self.charRect = pygame.Rect(475, 300, 20, 30)
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
    def reset(self, resetPlayerPos=True):
        gameManager.reset()
        if resetPlayerPos:
            self.x = 475
            self.y = level.lowestPoint-230
        self.xVel = 0
        self.yVel = 0
        self.homeTo = (0,0)
        level.changeLevel(resetPlayerPos)
        level.levelPosx, level.levelPosy = self.x, self.y 
        self.kTime = 0      
        self.powerUps = []                
    def changeX(self, speed): 
        self.x+=speed
        self.walkAnimateFrame += abs(self.xVel)/7
        if self.walkAnimateFrame >= 4:
            self.walkAnimateFrame = 0
        if self.x < 0:
            self.x = 0
        level.levelPosx=self.x
    def changeXVel(self, speed, isRight):
        self.isRight = isRight
        if isRight:
            self.xVel += speed
            if self.xVel > self.maxSpeed and not (keys[pygame.K_LSHIFT] or self.homeTo!=(0,0)):
                self.xVel -= speed
                if self.xVel > self.maxSpeed:
                    self.xVel-=self.decelSpeed
            elif self.xVel > self.maxBoost and (keys[pygame.K_LSHIFT] or self.homeTo!=(0,0)):
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
            if self.xVel < -self.maxSpeed and not (keys[pygame.K_LSHIFT] or self.homeTo!=(0,0)):
                self.xVel += speed
                if self.xVel < -self.maxSpeed:
                    self.xVel+=self.decelSpeed
            elif self.xVel < -self.maxBoost and (keys[pygame.K_LSHIFT] or self.homeTo!=(0,0)):
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


        self.changeX(self.xVel)
        
        if self.xVel > 0:
            level.levelPosx, level.levelPosy = self.x+0.1, self.y-0.1
            if level.checkCollision(self.charRect):
                movedUp = False
                for i in range(10):
                    level.levelPosy-=1
                    if not level.checkCollision(self.charRect) and not movedUp and not keys[pygame.K_LCTRL]:
                        level.levelPosx+=1
                        movedUp = True

                if not movedUp:
                    level.levelPosy+=10
                    self.xVel=0
                    self.touchGround = level.checkCollision(self.charRect)
                    while self.touchGround:
                        self.x-=0.1
                        level.levelPosx = self.x
                        self.touchGround = level.checkCollision(self.charRect)
                    if (keys[pygame.K_LCTRL]):
                        self.yVel = 0
                        self.climbedLastFrame=True
                        if keys[pygame.K_w] or keys[pygame.K_UP]:
                            self.yVel = -3
                            level.levelPosy -= 30
                            level.levelPosx += 1
                            if not level.checkCollision(self.charRect):
                                self.yVel = -7
                            level.levelPosy += 30
                            level.levelPosx -= 1
                        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                            self.yVel = 3
                    
        if self.xVel < 0:
            level.levelPosx, level.levelPosy = self.x-0.1, self.y-0.1
            if level.checkCollision(self.charRect):
                movedUp = False
                for i in range(10):
                    level.levelPosy-=1
                    if not level.checkCollision(self.charRect) and not movedUp and not keys[pygame.K_LCTRL]:
                        level.levelPosx-=1
                        movedUp = True
                if not movedUp:
                    level.levelPosy+=10
                    self.xVel=0
                    self.touchGround = level.checkCollision(self.charRect)
                    while self.touchGround:
                        self.x+=0.1
                        level.levelPosx = self.x
                        self.touchGround = level.checkCollision(self.charRect)
                    if (keys[pygame.K_LCTRL]):
                        self.yVel = 0
                        self.climbedLastFrame=True
                        
                        if keys[pygame.K_w] or keys[pygame.K_UP]:
                            self.yVel = -3
                            level.levelPosy -= 30
                            level.levelPosx -= 1
                            if not level.checkCollision(self.charRect):
                                self.yVel = -7
                            level.levelPosy += 30
                            level.levelPosx += 1
                        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                            self.yVel = 3
        

    def gravity(self):
        if self.homeTo != (0,0):
            self.homingCoolDown-=1
            if self.homingCoolDown==0:
                self.homeTo=(0,0)
        level.levelPosy = round(level.levelPosy, 2)
        if level.levelPosy > level.lowestPoint:
            self.die()
        #if self.homeTo == (0,0):
        for i in range(int(self.yVel)):
            self.y+=1
            level.levelPosx, level.levelPosy = self.x, self.y
            if level.checkCollision(self.charRect):
                self.yVel = 0
                self.jumpsLeft = 2
                self.stomp = False
                player.decelSpeed = 0.2
                #self.y-=0.1
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
            elif self.semied and not keys[pygame.K_SPACE]:
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
    def process(self):
        level.levelPosx, level.levelPosy = self.x, self.y

        if self.maxBoost > self.defaultBoost and self.homeTo == (0,0):
            self.maxBoost -= self.decelSpeed
        
        if self.stomp:
            self.teminalVelocity = 25
        else:
            self.teminalVelocity = 17

        self.gravity()
        if self.homeTo != (0,0):
            self.homingTo()

    def homingTo(self):
        if level.levelPosx < self.homeTo[0]:
            if self.homeRight:
                self.changeXVel(self.homeSpeed, True)
            else:
                self.xVel = 0
                self.changeX(self.homeTo[0] - level.levelPosx)
        elif level.levelPosx > self.homeTo[0]:
            if not self.homeRight:
                self.changeXVel(self.homeSpeed, False)
            else:
                self.xVel = 0
                self.changeX((level.levelPosx - self.homeTo[0])*-1)
        if level.levelPosy < self.homeTo[1]:
            if self.homeDown:
                    self.yVel += self.homeSpeed
            else:
                self.yVel = 0
                self.yVel -= level.levelPosy - self.homeTo[1]
        elif level.levelPosy > self.homeTo[1]:
            if not self.homeDown:
                self.yVel -= self.homeSpeed
            else:
                self.yVel = 0
                self.yVel += self.homeTo[1] - level.levelPosy
        
    def jump(self):
        level.levelPosy+=1
        if (self.touchGround or self.kTime>0) and self.jumpsLeft > 0:
            self.yVel = -self.jumpPower
            self.kTime=0
            self.jumpsLeft-=1
        elif self.homeTo == (0,0):
            print(level.checkCollision(self.homingRange, False, [9]))
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
        win.blit(self.animate(), (self.charRect.x-5, self.charRect.y))

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
        self.changeLevel()
        self.trimLevel()
        self.offset = 1540
        self.switch = False
    def checkCollision(self, rectToCheck, useTrim=True, tileToCheck=[0, 10]):
        collided = False
        if useTrim:
            for tile in self.trimmedLevel[::-1]:
                #print(tile.y, self.levelPosy+20)
                if tile.x < self.levelPosx+rectToCheck.width and tile.x > self.levelPosx-rectToCheck.width and tile.rect.y < player.charRect.y+300 and tile.rect.y > player.charRect.y-300:
                    tile.update()
                    if tile.tileID in tileToCheck:
                        if tile.checkCollision(rectToCheck):
                            player.stomp = False
                            collided = True
                            break
        else:
            for tile in self.onScreenLevel[::-1]:
                #print(tile.y, self.levelPosy+20)
                if tile.x < self.levelPosx+rectToCheck.width and tile.x > self.levelPosx-rectToCheck.width and tile.rect.y < player.charRect.y+300 and tile.rect.y > player.charRect.y-300:
                    tile.update()
                    if tile.tileID in tileToCheck:
                        if tile.checkCollision(rectToCheck):
                            player.stomp = False
                            collided = True
                            break
        return collided
    def changeLevel(self, resetPlayerPos=True, reloadLevel=False):
        if self.worldXLast != worldX or reloadLevel:
            self.worldXLast, self.worldYLast = worldX, worldY
            t, f = True, False
            self.levels = []
            with open(f'levels/{worldX}-{worldY}.csv', 'r') as csv_file:
                # Create a CSV reader object
                csv_reader = csv.reader(csv_file)
                tiles = list(csv_reader)

                # Loop through the rows in the CSV file
                for y, row in enumerate(tiles):
                    for x in range(len(row)):
                        if tiles[y][x] != "-1":
                            self.levels.append(Tile(x*20, y*20, int(tiles[y][x])))
                            if y*20+185 > self.lowestPoint:
                                self.lowestPoint = y*20+185
            self.levelVis = pygame.Surface((len(tiles[0])*20, len(tiles)*20))
            self.levelVis.fill(WHITE)
            tilesLoaded = 0
            groundTiles = ["0", "2"]
            if not self.quickDraw:
                for tile in self.levels:
                    if tile.tileID == "3" and resetPlayerPos:
                        spawnPos = self.getSpawn()
                        player.x, player.y = spawnPos[0], spawnPos[1]
                    if tile.tileID != "-1":
                        win.fill(BLACK)
                        win.blit(bigFont.render(f"Loading Level: {str(int((tilesLoaded/len(self.levels))*100))}% - {tilesLoaded}/{len(self.levels)}", True, WHITE), (0,90))
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                run = False
                                quit()
                            elif event.type == pygame.VIDEORESIZE:
                                # This event is triggered when the window is resized
                                w, h = event.w, event.h
                        window.blit(win, (0,0))
                        pygame.display.flip()
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
                            if tiles[int(tile.y/20)-1][int(tile.x/20)] in groundTiles:
                                above = True
                        if tile.y/20!=len(tiles)-1:
                            if tiles[int(tile.y/20)+1][int(tile.x/20)] in groundTiles:
                                below = True
                        if tile.x!=0:
                            if tiles[int(tile.y/20)][int(tile.x/20)-1] in groundTiles:
                                left = True
                        if tile.x/20!=len(row)-1:
                            if tiles[int(tile.y/20)][int(tile.x/20)+1] in groundTiles:
                                right = True
                        if tiles[int(tile.y/20)][int(tile.x/20)] == "0":
                            # Get the corresponding image based on neighbor pattern
                            neighbors = (above, below, left, right)
                            self.levels[tilesLoaded].image = tileImages[neighbor_image_map.get(neighbors, 6)]
                            self.levelVis.blit(tileImages[neighbor_image_map.get(neighbors, 6)], (self.levels[tilesLoaded].x, self.levels[tilesLoaded].y))
                            if neighbor_image_map.get(neighbors, 6) == 10:
                                tile.toBeDeleted = True
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "6":
                            self.levelVis.blit(tileImages[7], (self.levels[tilesLoaded].x, self.levels[tilesLoaded].y))
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "4":
                            self.levelVis.blit(tileImages[8], (self.levels[tilesLoaded].x, self.levels[tilesLoaded].y))
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "5":
                            self.levelVis.blit(tileImages[16], (self.levels[tilesLoaded].x, self.levels[tilesLoaded].y))
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "7":
                            self.levelVis.blit(tileImages[17], (self.levels[tilesLoaded].x, self.levels[tilesLoaded].y))
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "8":
                            self.levelVis.blit(tileImages[15], (self.levels[tilesLoaded].x, self.levels[tilesLoaded].y))
                        tilesLoaded+=1
        else:
            for tile in self.levels:
                tile.reload()
            if resetPlayerPos:
                spawnPos = self.getSpawn()
                player.x, player.y = spawnPos[0], spawnPos[1]

    def trimLevel(self):
        self.trimmedLevel = []
        self.onScreenLevel = []
        for tile in self.levels:
            #print(tile.y, self.levelPosy+20)
            if tile.rect.x > 400 and tile.rect.x < 550 and tile.rect.y > 200 and tile.rect.y < 400:
                self.trimmedLevel.append(tile)
                self.onScreenLevel.append(tile)
            elif tile.rect.x > -20 and tile.rect.x < 980 and tile.rect.y > -20 and tile.rect.y < 620:
                self.onScreenLevel.append(tile)
    
    def getSpawn(self):
        for tilesLoaded, tile in enumerate(self.levels):
            if tile.tileID == 3:
                return (self.levels[tilesLoaded].x, self.levels[tilesLoaded].y+160)
        return (0,0)

    def draw(self):
        win.blit(self.levelVis, (-self.levelPosx+475,-self.levelPosy+475))

class semiLevel:
    def __init__(self):
        pass
    def checkCollision(self, rectToCheck, tileToCheck=1):
        feetRect = pygame.Rect(475, player.charRect.y+29, 20, 1)
        collided = False
        if player.yVel >= 0:
            for tile in level.trimmedLevel:
                tile.update()
                if tile.x < level.levelPosx+20 and tile.x > level.levelPosx-20 and tile.rect.y < player.charRect.y+50 and tile.rect.y > player.charRect.y-20:
                    if tile.tileID == tileToCheck and not collided:
                        if tile.checkCollisionRect(feetRect):
                            collided = True
                            break
        return collided
    def draw(self):
        #win.blit(self.image, (-level.levelPosx+475,0))
        pass

class Tile:
    def __init__(self, x, y, tileID):
        self.x, self.y = x, y
        self.tileID = tileID
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.image = pygame.Surface((0,0))
        self.popped = False
        self.toBeDeleted = False
        self.popTimer = 0
    def update(self):
        self.rect.x = self.x-level.levelPosx+475
        self.rect.y = self.y-level.levelPosy+475
        if self.toBeDeleted:
            level.levels.remove(self)
        if self.popped and self.tileID in [9]:
            if not self in level.onScreenLevel:
                self.popped = False
        
    def isInSpace(self, x, y):
        return self.x == x and self.y == y
    def reload(self):
        self.popped = False
    def draw(self):
        if self.rect.x > -20 and self.rect.x < 960 and self.rect.y > -20 and self.rect.y < 600:
            if level.quickDraw:
                if self.tileID == 0:
                    if self.y == level.lowestPoint-185:
                        pygame.draw.rect(win, BLACK, pygame.Rect(self.rect.x, self.rect.y, 20, 600-self.rect.y))
                    else:
                        pygame.draw.rect(win, BLACK, self.rect)
                elif self.tileID == 4:
                    pygame.draw.rect(win, BLUE, self.rect)
                elif self.tileID == 8:
                    pygame.draw.rect(win, GREY, self.rect)
                elif self.tileID == 5:
                    pygame.draw.rect(win, GREEN, self.rect)
                elif self.tileID == 6:
                    pygame.draw.rect(win, YELLOW, self.rect)
                elif self.tileID == 7:
                    pygame.draw.rect(win, BROWN, self.rect)
            
            if self.tileID == 1:
                pygame.draw.rect(win, RED, self.rect)
            elif self.tileID == 2:
                pygame.draw.rect(win, PURPLE, self.rect)
            elif self.tileID == 9 and not self.popped:
                if player.homeTo == (self.x, self.y+160):
                    pygame.draw.rect(win, RED, self.rect)
                else:
                    pygame.draw.rect(win, CYAN, self.rect)
            elif self.tileID == 9 and self.popped:
                if player.homeTo == (self.x, self.y+160):
                    pygame.draw.rect(win, PINK, self.rect)
            elif self.tileID == 10:
                pygame.draw.rect(win, PINK, self.rect)
            elif self.tileID == 11 and not self.popped:
                pygame.draw.rect(win, ORANGE, self.rect)
            elif self.tileID == 12 and not self.popped:
                pygame.draw.rect(win, GOLD, self.rect)
            elif self.tileID == 13 and not self.popped:
                pygame.draw.rect(win, MAGENTA, self.rect)
            elif self.tileID == 14:
                pygame.draw.rect(win, LIME, self.rect)

        
        if self.popped and self.popTimer>0:
            self.popTimer-=1
            if self.popTimer==0:
                self.popped = False
            
    def checkCollision(self, collider):
        collided = self.rect.colliderect(collider)
        if collided and collider == player.charRect:
            # if not self.popped:
            #     player.homeTo = (0,0)
            player.canHomingAttck = True
            if self.tileID == 4:
                player.yVel = -20
                player.xVel = 0
            elif self.tileID == 8:
                player.yVel = 20
                player.xVel = 0
            elif self.tileID == 6:
                player.yVel = -13
                player.xVel = 0
            elif self.tileID == 2:
                player.die()
            elif self.tileID == 5:
                if player.yVel > 0:
                    player.yVel = 0
                player.maxBoost = 20
                player.xVel = 13
            elif self.tileID == 7:
                if player.yVel > 0:
                    player.yVel = 0
                player.maxBoost = 20
                player.xVel = -13
            elif self.tileID == 9 and not self.popped:
                player.yVel = -10
                player.xVel = 0
                self.popped = True
                player.homeTo = (0,0)
                self.popTimer = 360
            elif self.tileID == 10:
                gameManager.speed = 0
                player.xVel=0
                player.jumpPower = 17
            elif self.tileID == 11 and not self.popped:
                player.powerUps.append(PowerUp(0, 240))
                self.popped = True
            elif self.tileID == 12 and not self.popped:
                gameManager.collectables+=1
                self.popped = True
            elif self.tileID == 13 and not self.popped:
                gameManager.rareCollectables+=1
                self.popped = True
            elif self.tileID == 14:
                if player.xVel > 0:
                    player.yVel=-abs(player.xVel)*1.5
                else:
                    playerInTile = True
                    player.xVel=0
                    while playerInTile:
                        player.changeX(1)
                        self.update()
                        playerInTile = self.checkCollision(player.charRect)


        elif collided and collider == player.homingRange and not self.popped:
            if self.tileID == 9:
                player.homeTo = (self.x, self.y+160)
                player.maxBoost = 20
                player.homingCoolDown = 30
                
                if level.levelPosx < player.homeTo[0]:
                    player.homeRight = True
                elif level.levelPosx > player.homeTo[0]:
                    player.homeRight = False
                if level.levelPosy < player.homeTo[1]:
                    player.homeDown = True
                elif level.levelPosy > player.homeTo[1]:
                    player.homeDown = False
        elif collided and collider == player.homingRange and self.popped:
            collided = False

                

        return collided
    def checkCollisionRect(self, collider):
        return self.rect.colliderect(collider)

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
        

def redrawScreen():
        
    win.fill(WHITE)
    level.draw()
    
    #spikes.draw() 

    for tile in level.onScreenLevel:
        tile.draw()

    player.draw()


    pygame.draw.rect(win, WHITE, pygame.Rect(0,0, 65, 25))
    win.blit(smallFont.render("FPS: " + str(int(clock.get_fps())), True, (0, 0, 0)), (0,0))
    # pygame.draw.rect(win, WHITE, pygame.Rect(0,30, 120, 25))
    # win.blit(smallFont.render("YVEL: " + str(player.yVel), True, (0, 0, 0)), (0,30))
    # pygame.draw.rect(win, WHITE, pygame.Rect(0,60, 120, 25))
    # win.blit(smallFont.render("XVEL: " + str(player.xVel), True, (0, 0, 0)), (0,60))
    pygame.draw.rect(win, WHITE, pygame.Rect(0,90, 120, 25))
    win.blit(smallFont.render("HOMETO: " + str(player.homeTo), True, (0, 0, 0)), (0,90))

    if keys[pygame.K_RCTRL]:
        for i, image in enumerate(tileImages):
            win.blit(image, (0 + i*20, 0))
            win.blit(smallFont.render(str(i), True, RED), (0 + i*20, 0))
    if level.quickDraw:
        win.blit(smallFont.render("QUICK LOAD MODE ENABLED - LCTRL + T to reload", True, RED), (0, 540))

    for y, log in enumerate(debugLog):
        log.draw(y)

    window.blit(pygame.transform.scale(win, (w, h)), (0,0))    
    pygame.display.flip()

gameManager = GameManager()
player = Player()
keys = pygame.key.get_pressed()
level = Level()
player.reset()
semiLevel = semiLevel()

debugLog = [DebugLogText("TEST", 120)]


spaceHeld = False
stompHeld = False

stallFrames = False
#stallFrames = True


run = True
# Main game loop
while run:
    waiting = True
    while waiting  and stallFrames:
        redrawScreen()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
        elif event.type == pygame.MOUSEWHEEL:
            scrolly = event.y
        elif event.type == pygame.VIDEORESIZE:
            # This event is triggered when the window is resized
            w, h = event.w, event.h

    
    #mouse getters
    clicked = pygame.mouse.get_pressed(num_buttons=3)
    posx, posy = pygame.mouse.get_pos()

    level.trimLevel()
    
    keys = pygame.key.get_pressed()

    if spaceHeld:
        spaceHeld = keys[pygame.K_SPACE]
    if stompHeld:
        stompHeld = keys[pygame.K_DOWN] or keys[pygame.K_s]

    player.process()
    if keys[pygame.K_SPACE] and not spaceHeld:
        player.jump()
        spaceHeld = True
    
    player.jumpPower = 11

    if ((keys[pygame.K_a] or keys[pygame.K_LEFT]) and not (keys[pygame.K_d] or keys[pygame.K_RIGHT])) or ((keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not (keys[pygame.K_a] or keys[pygame.K_LEFT])):
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            player.changeXVel(gameManager.speed/10, False)
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            player.changeXVel(gameManager.speed/10, True)
    elif player.xVel > 0:
        player.xVel-=player.decelSpeed
        player.changeXVel(0, True)
        player.boostDirection = 0
    elif player.xVel < 0:
        player.xVel+=player.decelSpeed
        player.changeXVel(0, False)
        player.boostDirection = 0
        player.canBoost = True
    elif player.conveyorBonus != 0:
        print(player.conveyorBonus)
        print(player.conveyorBonus>0)
        player.changeXVel(0, player.conveyorBonus>0)
    
    # if not player.climbedLastFrame and player.kTime < 8:
    #     if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and not stompHeld:
    #         player.stomp = True
    #         player.yVel = 20
    #         stompHeld = True

    if keys[pygame.K_r]:
        if keys[pygame.K_LCTRL]:
            if keys[pygame.K_LSHIFT]:
                level.changeLevel(True, True)
                debugLog.append(DebugLogText("Full Reload"))
                player.reset()
            elif keys[pygame.K_LALT]:
                debugLog.append(DebugLogText("QuickDraw Load"))
                level.quickDraw = True
                level.changeLevel(True, True)
                player.reset()
            else:
                debugLog.append(DebugLogText("Advanced Reload"))
                level.changeLevel(False, True)
                print(f"1 {player.x}")
                player.reset(False)
                print(f"2 {player.x}")
            w, h = 960, 600
            window = pygame.display.set_mode((960, 600), pygame.RESIZABLE)
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

    
    
    if keys[pygame.K_LCTRL]:
        if keys[pygame.K_q]:
            worldX -= 1
            if worldX < 0:
                worldX = 2
            level.changeLevel()
            semiLevel.changeLevel()
            player.reset()
            waiting = True
            while waiting:
                redrawScreen()
                for event in pygame.event.get():
                    if event.type == pygame.KEYUP:
                        waiting = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        run = False
                        quit()
    
    gameManager.speed = 3
    
    for tile in level.levels:
        tile.update()
        

    #redraw win
    redrawScreen()
    # Set the framerate
    deltaTime = clock.tick(60)/10

