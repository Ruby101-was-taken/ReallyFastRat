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
pygame.display.set_caption("Platformer")
pygame.display.set_icon(pygame.image.load('icon.png'))

logo=[pygame.image.load('logo/logosubless.png'), pygame.image.load('logo/logoSUB.png'), pygame.image.load('logo/logoBGless.png')]

# for i in range(500):
#     win.fill(LOGORED)
#     if i<=100:
#         win.blit(logo[0], (int(960/2)-168, int(600/2)-48))
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 run = False
#                 quit()
#             elif event.type == pygame.VIDEORESIZE:
#                 # This event is triggered when the window is resized
#                 w, h = event.w, event.h
#     elif i<200:
#         subLength = int(960/2)-168+40
#         subHeight = int(600/2)-40
#         win.blit(logo[0], (int(960/2)-168, int(600/2)-48))
#         win.blit(logo[1], (subLength, (subHeight*i / 100)-subHeight))
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 run = False
#                 quit()
#             elif event.type == pygame.VIDEORESIZE:
#                 # This event is triggered when the window is resized
#                 w, h = event.w, event.h
#     elif i<500:
#         win.blit(logo[0], (int(960/2)-168, int(600/2)-48))
#         win.blit(logo[1], (subLength, (subHeight*200 / 100)-subHeight))
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 run = False
#                 quit()
#             elif event.type == pygame.VIDEORESIZE:
#                 # This event is triggered when the window is resized
#                 w, h = event.w, event.h
    
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

#LOAD IMAGES 
playerImages = [
    pygame.image.load("player/player.png")
]

slope = pygame.image.load("objects/slope.png")

tile_width = 20
tile_height = 20  # Replace with your tile height

tileSheet = pygame.image.load("tilemap/sampleTiles.png")


def sliceTilemap(sheet, w, h):
    spliedImages = []  # This list will hold your individual tiles
    sheet = sheet.convert_alpha()
    for y in range(0, sheet.get_height(), h):
        for x in range(0, sheet.get_width(), w):
            tile = sheet.subsurface(pygame.Rect(x, y, w, h)).convert_alpha()
            spliedImages.append(tile.convert_alpha()) 
    
    return spliedImages

tileImages = sliceTilemap(tileSheet, 20, 20)
spikeImages = sliceTilemap(pygame.image.load("tilemap/spikeTiles.png"), 20, 20)
bridgeImages = sliceTilemap(pygame.image.load("tilemap/bridgeTiles.png"), 20, 20)

slope = sliceTilemap(slope, 20, 20)





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
        self.speed = 0.5
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
        self.rectAsSurface = pygame.Surface((20,20))
        self.rectAsSurface.fill((255,0,0))
        self.image = pygame.image.load("player.png")
        self.kTime = 0
        self.climbedLastFrame=False
        self.teminalVelocity = 17
        self.decelSpeed = 0.4

        self.topSpeed = 3

        self.jumpsLeft = 2
        self.jumpPower = 11

        self.isRight = False

        self.powerUps = []
    def reset(self, resetPlayerPos=True):
        gameManager.reset()
        if resetPlayerPos:
            self.x = 475
            self.y = level.lowestPoint-230
        self.xVel = 0
        self.yVel = 0
        level.changeLevel(resetPlayerPos)
        level.levelPosx, level.levelPosy = self.x, self.y 
        self.kTime = 0      
        self.powerUps = []                
    def changeX(self, speed): 
        canMoveUp = False

        for i in range(int(abs(speed))):
            level.levelPosx+=self.isPosNeg(speed)
            if level.checkCollision(self.charRect, True):
                canMoveUp = False
                
                for i in range(8):
                    if not level.checkCollision(self.charRect, True) and not canMoveUp:
                        canMoveUp = True
                    elif not canMoveUp:
                        level.levelPosy-=1
                if not canMoveUp:
                    level.levelPosy+=8
                    level.levelPosx-=self.isPosNeg(speed)
                    self.xVel = 0

                
        if level.levelPosx < 0:
            level.levelPosx = 0
        self.x = level.levelPosx
    def changeXVel(self, speed, isPlayerInput, isRight):
        if isPlayerInput:
            self.isRight = isRight

        if not isPlayerInput or abs(self.xVel) < self.topSpeed:
            if isRight:
                self.xVel += speed
            elif not isRight:
                self.xVel += -speed

        if abs(self.xVel) > 0.1:
            self.xVel-=self.decelSpeed*self.isPosNeg(self.xVel)
        else:
            self.xVel = 0
        
        round(self.xVel, 2)
            
        level.levelPosx, level.levelPosy = self.x, self.y
    

    def isPosNeg(self, num):
        if num!= 0:
            return abs(num)/num
        else:
            return 0
        

    def gravity(self):
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
        
            

        level.checkCollision(self.charRect, True, [2,4,5,6,7])

        


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
    def update(self):
        level.levelPosx, level.levelPosy = self.x, self.y
        self.changeX(self.xVel)
        self.gravity()
        
    def jump(self):
        level.levelPosy+=1
        if (self.touchGround or self.kTime>0) and self.jumpsLeft > 0:
            self.yVel = -self.jumpPower
            self.kTime=0
            self.jumpsLeft-=1
            audioPlayer.playSound(jump)
        level.levelPosy-=1

    def animate(self):
        returnImage = playerImages[0]
        
        return returnImage

    def draw(self):
        pygame.draw.rect(win, RED, self.charRect)
        #win.blit(self.animate(), (self.charRect.x-5, self.charRect.y))

        
    
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
    def checkCollision(self, rectToCheck, useTrim=True, tileToCheck=[0, 8, 9, 10, 11]):
        collided = False
        if useTrim:
            for tile in self.trimmedLevel[::-1]:
                if tile.x < self.levelPosx+rectToCheck.width and tile.x > self.levelPosx-rectToCheck.width and tile.rect.y < player.charRect.y+300 and tile.rect.y > player.charRect.y-300:
                    tile.update(True)
                    if tile.tileID in tileToCheck:
                        if tile.checkCollision(rectToCheck):
                            player.stomp = False
                            collided = True
                            break
        else:
            for tile in self.onScreenLevel[::-1]:
                if tile.x < self.levelPosx+rectToCheck.width and tile.x > self.levelPosx-rectToCheck.width and tile.rect.y < player.charRect.y+300 and tile.rect.y > player.charRect.y-300:
                    tile.update(True)
                    if tile.tileID in tileToCheck:
                        if tile.checkCollision(rectToCheck):
                            player.stomp = False
                            collided = True
                            break
        return collided
    def changeLevel(self, resetPlayerPos=True, reloadLevel=False):
        groundTiles = ["0", "2", "8", "9", "10", "11", "14", "15", "16", "17"]
        if self.worldXLast != worldX or reloadLevel:
            self.worldXLast, self.worldYLast = worldX, worldY
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
            self.levelVis = pygame.Surface((len(tiles[0])*20, (len(tiles)*20+300)), pygame.SRCALPHA)
            self.levelVis.fill((0,0,0,0))
            tilesLoaded = 0
            if not self.quickDraw:
                loadingText = ""
                for tile in self.levels:
                    if tile.tileID == "3" and resetPlayerPos:
                        spawnPos = self.getSpawn()
                        player.x, player.y = spawnPos[0], spawnPos[1]
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
                            self.getTileImage(tile, tiles, "0", row, tilesLoaded, tileImages)
                        if tiles[int(tile.y/20)][int(tile.x/20)] == "1":
                            self.getTileImage(tile, tiles, "1", row, tilesLoaded, bridgeImages, ["0", "1"])
                        if tiles[int(tile.y/20)][int(tile.x/20)] == "2":
                            self.getTileImage(tile, tiles, "2", row, tilesLoaded, spikeImages)
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "5":
                            tile.image = tileImages[7]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "4":
                            tile.image = tileImages[8]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "5":
                            tile.image = tileImages[16]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "7":
                            tile.image = tileImages[17]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "14":
                            tile.image = tileImages[14]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "15":
                            tile.image = tileImages[15]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "16":
                            tile.image = tileImages[17]
                        elif tiles[int(tile.y/20)][int(tile.x/20)] == "17":
                            tile.image = tileImages[18]
                        tilesLoaded+=1
                    
            else:
                for tile in self.levels:
                    above, below, left, right = False, False, False, False
                    if tile.tileID == 0:# Check neighbors
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

                        if above and below and left and right:
                            tile.toBeDeleted = True

        else:
            for tile in self.levels:
                tile.reload()
            if resetPlayerPos:
                spawnPos = self.getSpawn()
                player.x, player.y = spawnPos[0], spawnPos[1]
    
    def getTileImage(self, tile, tiles, typeNum:str, row, tilesLoaded, tilesToBeUsed, groundTiles=["0", "2", "8", "9", "10", "11"]):
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
        if tiles[int(tile.y/20)][int(tile.x/20)] == typeNum:
            # Get the corresponding image based on neighbor pattern
            neighbors = (above, below, left, right)
            self.levels[tilesLoaded].image = tilesToBeUsed[neighbor_image_map.get(neighbors, 6)]
            tile.image = tilesToBeUsed[neighbor_image_map.get(neighbors, 6)].convert_alpha()
            
            newImage = pygame.Surface((20,20), pygame.SRCALPHA)
            newImage.blit(tile.image, (0,0))


            
            if neighbor_image_map.get(neighbors, 6) in [18, 19, 20, 24, 25, 26] and tile.y == self.lowestPoint-185:
                if neighbor_image_map.get(neighbors, 6) == 18:
                    tile.repeatImage = tilesToBeUsed[9]
                elif neighbor_image_map.get(neighbors, 6) == 20:
                    tile.repeatImage = tilesToBeUsed[11]
                else:
                    tile.repeatImage = tilesToBeUsed[10]


            
            #right side
            if tile.y!=0 and tile.x/20!=len(row)-1 and above and right:
                if not tiles[int(tile.y/20)-1][int(tile.x/20)+1] in groundTiles:
                    newImage.blit(tilesToBeUsed[5], (0,0))
            if tile.y/20!=len(tiles)-1 and tile.x/20!=len(row)-1 and below and right:
                if not tiles[int(tile.y/20)+1][int(tile.x/20)+1] in groundTiles:
                    newImage.blit(pygame.transform.rotate(tilesToBeUsed[5], -90), (0,0))

            #left side
            if tile.y!=0 and tile.x!=0 and above and left:
                if not tiles[int(tile.y/20)-1][int(tile.x/20)-1] in groundTiles:
                    newImage.blit(pygame.transform.rotate(tilesToBeUsed[5], 90), (0,0))
            if tile.y/20!=len(tiles)-1 and tile.x!=0 and below and left:
                if not tiles[int(tile.y/20)+1][int(tile.x/20)-1] in groundTiles:
                    newImage.blit(pygame.transform.rotate(tilesToBeUsed[5], 180), (0,0))

            
            tile.image = newImage
            #self.levelVis.blit(tileImages[neighbor_image_map.get(neighbors, 6)], (self.levels[tilesLoaded].x, self.levels[tilesLoaded].y))
            if neighbor_image_map.get(neighbors, 6) == 10:
                tile.toBeDeleted = True


    def trimLevel(self):
        self.trimmedLevel = []
        self.onScreenLevel = []
        for tile in self.levels:
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

        for tile in self.onScreenLevel:
            tile.update(True)
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
    def __init__(self, x, y, tileID, image=pygame.Surface((0,0)), repeatImage=pygame.Surface((0,0))):
        self.x, self.y = x, y
        self.tileID = tileID
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.image = image
        self.repeatImage = repeatImage
        self.popped = False
        self.toBeDeleted = False
        self.popTimer = 0
        if self.tileID in [8, 9, 10, 11]:
            self.mask = pygame.mask.from_surface(slope[self.tileID-8])
            print(self.tileID-8)
        self.hasBeenDrawn = self.tileID in [6,7] #this list is the tiles that draw on the fly rather than being static
    def update(self, onScreen=False):
        self.rect.x = self.x-level.levelPosx+475
        self.rect.y = self.y-level.levelPosy+475
        if self.popped and self.tileID in [9]:
            if not self in level.onScreenLevel:
                self.popped = False
        if not self.hasBeenDrawn and onScreen:
            level.levelVis.blit(self.image.convert_alpha(), (self.x, self.y))
            if self.y == level.lowestPoint-185:
                for i in range(15):
                    level.levelVis.blit(self.repeatImage, (self.x, self.y+(20*(i+1))))
            
            self.hasBeenDrawn = True
            if self.toBeDeleted:
                level.levels.remove(self)
        

        
    def isInSpace(self, x, y):
        return self.x == x and self.y == y
    def reload(self):
        self.popped = False
    def draw(self):
        if self.rect.x > -20 and self.rect.x < 960 and self.rect.y > -20 and self.rect.y < 600:
            pass
            if level.quickDraw:
                if self.tileID == 0:
                    if self.y == level.lowestPoint-185:
                        pygame.draw.rect(win, BLACK, pygame.Rect(self.rect.x, self.rect.y, 20, 600-self.rect.y))
                    else:
                        pygame.draw.rect(win, BLACK, self.rect)
                elif self.tileID == 4:
                    pygame.draw.rect(win, BLUE, self.rect)
                elif self.tileID == 5:
                    pygame.draw.rect(win, YELLOW, self.rect)
                elif self.tileID == 8:
                    win.blit(slope, (self.rect.x, self.rect.y))
                elif self.tileID == 2:
                    pygame.draw.rect(win, PURPLE, self.rect)
                elif self.tileID == 1:
                    pygame.draw.rect(win, RED, self.rect)
            
            if self.tileID == 6 and not self.popped:
                pygame.draw.rect(win, GOLD, self.rect)
            elif self.tileID == 7 and not self.popped:
                pygame.draw.rect(win, MAGENTA, self.rect)

        
        if self.popped and self.popTimer>0:
            self.popTimer-=1
            if self.popTimer==0:
                self.popped = False
    
            
    def checkCollision(self, collider):
        collided = self.rect.colliderect(collider)
        if collided and collider == player.charRect:
            player.canHomingAttck = True
            if self.tileID == 4:
                player.yVel = -20
                player.xVel = 0
            elif self.tileID == 5:
                player.yVel = -13
                player.xVel = 0
            elif self.tileID == 2:
                player.die()
            elif self.tileID == 6:
                if not self.popped:
                    gameManager.collectables+=1
                    self.popped = True
                else:
                    collided = False
            elif self.tileID == 7:
                if not self.popped:
                    gameManager.rareCollectables+=1
                    self.popped = True
                else:
                    collided = False
            elif self.tileID in [8, 9, 10, 11]:
                offset = ((collider.x - self.rect.x), (collider.y - self.rect.y)+10)
                collided = self.mask.overlap(pygame.mask.from_surface(player.rectAsSurface), offset) is not None
              


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

class InputSystem:
    def __init__(self) -> None:
        self.inputDict = {}
    def setKey(self, keyEnum, inputName:str):
        if inputName in self.inputDict:
            self.inputDict[inputName].append(keyEnum)
        else:
            self.inputDict[inputName] = [keyEnum]
    def keyEvent(self, inputName:str) -> bool:
        inputted = False
        for keyEnum in self.inputDict[inputName]:
            if keys[keyEnum]:
                inputted = True
        return inputted

class UICanvas:
    def __init__(self) -> None:
        self.UIComponents = []
    def addElement(self, element):
        self.UIComponents.append(element)
    def getElementByTag(self, tag:str):
        for element in self.UIComponents:
            if element.tag == tag:
                return element
    def draw(self):
        for element in self.UIComponents:
            element.draw()
    def update(self):
        for element in self.UIComponents:
            element.update()

class UIElement:
    def __init__(self, screenPos, tag:str) -> None:
        self.screenPos = screenPos
        self.tag = tag
        self.surface = pygame.Surface((0,0), pygame.SRCALPHA)
        self.show = True
    def toggleShow(self):
        self.show = not self.show
    def setShow(self, setTo:bool):
        self.show = setTo
    def moveTo(self, newPos):
        self.screenPos = newPos
    def draw(self):
        if self.show:
            win.blit(self.surface, self.screenPos)
    def update(self):
        pass

class UIText(UIElement):
    def __init__(self, screenPos, tag:str, text="", fontSize=10, colour=(0,0,0), padding=20) -> None:
        super().__init__(screenPos, tag)
        self.text = text
        self.fontSize = fontSize
        self.colour = colour
        self.font = pygame.font.SysFont("arial", self.fontSize)
        self.surface = self.font.render(text, True, self.colour)
        self.padding = padding

        self.surface = pygame.Surface((self.surface.get_width() + self.padding*2, self.surface.get_height() + self.padding*2))
    def updateText(self, newText:str, fontSize=None, colour=None):
        if fontSize!=None:
            self.fontSize = fontSize
        if colour!=None:
            self.colour = colour
        self.font = pygame.font.SysFont("arial", self.fontSize)
        textSurf = self.font.render(newText, True, self.colour)
        self.surface = textSurf.copy()
        self.surface = pygame.Surface((textSurf.get_width() + self.padding*2, textSurf.get_height() + self.padding*2))

        if self.bg.tag!="textBGEmpty":
            self.bg.updateSize(self.surface.get_width(),self.surface.get_height())
            self.bg.updateSurface()

        self.surface.blit(self.bg.surface, (0,0))
        self.surface.blit(textSurf, (self.padding,self.padding))
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
        self.rect = pygame.Rect(self.screenPos[0], self.screenPos[1], self.w, self.h)
        self.surface = pygame.Surface((w, h))
        if colour != None:
            self.colour = colour
        pygame.draw.rect(self.surface, self.colour, self.rect)
    def updateSurface(self):
        pygame.draw.rect(self.surface, self.colour, self.rect)
    def updateSize(self, w, h):
        self.w, self.h = w, h
        self.rect = pygame.Rect(self.screenPos[0], self.screenPos[1], self.w, self.h)
        self.surface = pygame.Surface((w, h))
        
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

audioPlayer.playMusic(music)

def redrawScreen():
        
    win.fill(WHITE)

    level.draw()
    

    for tile in level.onScreenLevel:
        tile.draw()

    player.draw()


    #pygame.draw.rect(win, WHITE, pygame.Rect(0,0, 65, 25))
    #win.blit(smallFont.render("FPS: " + str(int(clock.get_fps())), True, (0, 0, 0)), (0,0))

    if keys[pygame.K_RCTRL]:
        for i, image in enumerate(tileImages):
            win.blit(image, (0 + i*20, 0))
            win.blit(smallFont.render(str(i), True, RED), (0 + i*20, 0))
    if level.quickDraw:
        win.blit(smallFont.render("QUICK LOAD MODE ENABLED - LCTRL + T to reload", True, RED), (0, 540))

    for y, log in enumerate(debugLog):
        log.draw(y)

    ui.getElementByTag("FPSText").updateText("FPS: " + str(int(clock.get_fps())))
    ui.draw()

    window.blit(pygame.transform.scale(win, (w, h)), (0,0))    
    pygame.display.flip()

gameManager = GameManager()
player = Player()
keys = pygame.key.get_pressed()
level = Level()
player.reset()
semiLevel = semiLevel()

ui = UICanvas()
ui.addElement(UIText((0,0), "FPSText", "FPS:", 20, (0,0,0)))
ui.getElementByTag("FPSText").setBG((255,255,255))

debugLog = [DebugLogText("TEST", 120)]


spaceHeld = False
stompHeld = False

stallFrames = 0
frameAdvance = False
slashHeld = False

inputs = InputSystem()

inputs.setKey(pygame.K_SPACE, "Jump")
inputs.setKey(pygame.K_LEFT, "MoveLeft")
inputs.setKey(pygame.K_a, "MoveLeft")
inputs.setKey(pygame.K_RIGHT, "MoveRight")
inputs.setKey(pygame.K_d, "MoveRight")

run = True
# Main game loop,
while run:
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
        spaceHeld = inputs.keyEvent("Jump")
    if stompHeld:
        stompHeld = keys[pygame.K_DOWN] or keys[pygame.K_s]

    player.update()
    if inputs.keyEvent("Jump") and not spaceHeld:
        player.jump()
        spaceHeld = True
    
    player.jumpPower = 11

    if (inputs.keyEvent("MoveLeft") and not inputs.keyEvent("MoveRight")) or (inputs.keyEvent("MoveRight") and not inputs.keyEvent("MoveLeft")):
        if inputs.keyEvent("MoveLeft") and not inputs.keyEvent("MoveRight"):
            player.changeXVel(gameManager.speed, True, False)
        if inputs.keyEvent("MoveRight") and not inputs.keyEvent("MoveLeft"):
            player.changeXVel(gameManager.speed, True, True)
    else:
        player.changeXVel(0, False, player.isRight)
    
    

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
                player.reset(False)
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

    
    
    
    for tile in level.levels:
        tile.update()
        

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