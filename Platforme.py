import pygame, random, asyncio, os, csv

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
pygame.display.set_caption("A Solar Trip: Rock Destruction")
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

async def main():
    global w, h, window

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
            self.maxSpeed = speed
            self.maxBoost = speed*3
            self.defaultBoost = self.maxBoost
            self.teminalVelocity = 17
            self.boostDirection = 0
            self.canBoost = True
            self.decelSpeed = 0.2
            self.bonusXVel = 0

            self.jumpsLeft = 2

            self.stomp = False

            self.walkAnimateFrame = 0
            self.jumpAnimateFrame = 0
            self.isRight = True
        def reset(self):
            self.x = 475
            self.y = level.lowestPoint-230
            self.xVel = 0
            self.yVel = 0
            level.changeLevel()
            level.levelPosx, level.levelPosy = self.x, self.y 
            self.kTime = 0                      
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
                if self.xVel > self.maxSpeed and not keys[pygame.K_LSHIFT]:
                    self.xVel -= speed
                    if self.xVel > self.maxSpeed:
                        self.xVel-=self.decelSpeed
                elif self.xVel > self.maxBoost and keys[pygame.K_LSHIFT]:
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
                if self.xVel < -self.maxSpeed and not keys[pygame.K_LSHIFT]:
                    self.xVel += speed
                    if self.xVel < -self.maxSpeed:
                        self.xVel+=self.decelSpeed
                elif self.xVel < -self.maxBoost and keys[pygame.K_LSHIFT]:
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
                if level.checkCollision():
                    movedUp = False
                    for i in range(10):
                        level.levelPosy-=1
                        if not level.checkCollision() and not movedUp and not keys[pygame.K_LCTRL]:
                            level.levelPosx+=1
                            movedUp = True

                    if not movedUp:
                        level.levelPosy+=10
                        self.xVel=0
                        self.touchGround = level.checkCollision()
                        while self.touchGround:
                            self.x-=0.1
                            level.levelPosx = self.x
                            self.touchGround = level.checkCollision()
                        if (keys[pygame.K_LCTRL]):
                            self.yVel = 0
                            self.climbedLastFrame=True
                            if keys[pygame.K_w] or keys[pygame.K_UP]:
                                self.yVel = -3
                                level.levelPosy -= 30
                                level.levelPosx += 1
                                if not level.checkCollision():
                                    self.yVel = -7
                                level.levelPosy += 30
                                level.levelPosx -= 1
                            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                                self.yVel = 3
                        
            if self.xVel < 0:
                level.levelPosx, level.levelPosy = self.x-0.1, self.y-0.1
                if level.checkCollision():
                    movedUp = False
                    for i in range(10):
                        level.levelPosy-=1
                        if not level.checkCollision() and not movedUp and not keys[pygame.K_LCTRL]:
                            level.levelPosx-=1
                            movedUp = True
                    if not movedUp:
                        level.levelPosy+=10
                        self.xVel=0
                        self.touchGround = level.checkCollision()
                        while self.touchGround:
                            self.x+=0.1
                            level.levelPosx = self.x
                            self.touchGround = level.checkCollision()
                        if (keys[pygame.K_LCTRL]):
                            self.yVel = 0
                            self.climbedLastFrame=True
                            
                            if keys[pygame.K_w] or keys[pygame.K_UP]:
                                self.yVel = -3
                                level.levelPosy -= 30
                                level.levelPosx -= 1
                                if not level.checkCollision():
                                    self.yVel = -7
                                level.levelPosy += 30
                                level.levelPosx += 1
                            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                                self.yVel = 3
            
        def gravity(self):
            level.levelPosy = round(level.levelPosy, 2)
            if level.levelPosy > level.lowestPoint:
                self.die()

            for i in range(int(self.yVel)):
                self.y+=1
                level.levelPosx, level.levelPosy = self.x, self.y
                if level.checkCollision():
                    self.yVel = 0
                    self.jumpsLeft = 2
                    self.stomp = False
                    player.decelSpeed = 0.2
                    #self.y-=0.1
                    level.levelPosy = self.y
                    break
            for i in range(-int(self.yVel)):
                self.y-=1
                level.levelPosx, level.levelPosy = self.x, self.y
                self.checkCeiling()
            if not level.checkCollision():
                self.yVel+=0.5
                if self.yVel > self.teminalVelocity:
                    self.yVel = self.teminalVelocity
                self.kTime -= 1
                if self.kTime<0:
                    self.kTime=0
                    self.decelSpeed = 0.05
            
            level.levelPosy+=1
            self.touchGround = level.checkCollision()
            level.levelPosy-=1
            while self.touchGround:
                level.levelPosy = self.y+1
                if not level.checkCollision():
                    self.yVel=+1
                    self.y+=1
                    level.levelPosy = self.y
                    self.touchGround=False
                    self.kTime = 0
                else:
                    self.y-=0.1
                    level.levelPosy = self.y
                    self.touchGround = level.checkCollision()
                    self.kTime = defaultKTime
                    self.stomp = False
                    self.jumpsLeft = 2
            

            if semiLevel.checkCollision():
                level.levelPosy-=int(self.yVel)+1
                if not semiLevel.checkCollision():
                    level.levelPosy+=1
                    player.decelSpeed = 0.2
                    self.yVel = 0
                    self.touchGround = True
                    self.stomp = False
                    toochSemi = self.semied
                    self.semied = True
                    while not toochSemi:
                        level.levelPosy+=1
                        toochSemi = semiLevel.checkCollision()
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
            


            level.checkCollision([2, 4, 5, 6, 7, 8])



        def checkCeiling(self):
            level.levelPosy = self.y-1
            self.charRect.height = 1
            if level.checkCollision():
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

            if self.maxBoost > self.defaultBoost:
                self.maxBoost -= self.decelSpeed
            
            if self.stomp:
                self.teminalVelocity = 25
            else:
                self.teminalVelocity = 17

            self.gravity()
            
        def jump(self):
            level.levelPosy+=1
            if (self.touchGround or self.kTime>0) and self.jumpsLeft > 0:
                self.yVel = -11
                self.kTime=0
                self.jumpsLeft-=1
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
            elif self.yVel < 0:
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
            win.blit(self.animate(), (self.charRect.x-5, self.charRect.y))

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
            self.changeLevel()
            self.trimLevel()
        def checkCollision(self, tileToCheck=[0]):
            collided = False
            for tile in self.trimmedLevel:
                #print(tile.y, self.levelPosy+20)
                if tile.x < self.levelPosx+20 and tile.x > self.levelPosx-20 and tile.rect.y < player.charRect.y+300 and tile.rect.y > player.charRect.y-300:
                    tile.update()
                    if tile.tileID in tileToCheck:
                        if tile.checkCollision(player):
                            player.stomp = False
                            collided = True
                            break
            return collided
        def draw(self):
            pass
            #win.blit(self.image, (-self.levelPosx+475,0))
        def changeLevel(self):
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
        def trimLevel(self):
            self.trimmedLevel = []
            for tile in self.levels:
                #print(tile.y, self.levelPosy+20)
                if tile.rect.x > -20 and tile.rect.x < 960 and tile.rect.y > -20 and tile.rect.y < 600:
                    self.trimmedLevel.append(tile)
    class SemiLevel:
        def __init__(self):
            pass
        def checkCollision(self, tileToCheck=1):
            feetRect = pygame.Rect(475, player.charRect.y+29, 20, 1)
            collided = False
            if player.yVel >= 0:
                for tile in level.trimmedLevel:
                    tile.update()
                    if tile.x < level.levelPosx+20 and tile.x > level.levelPosx-20 and tile.rect.y < player.charRect.y+50 and tile.rect.y > player.charRect.y-20:
                        if tile.tileID == tileToCheck:
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
            if self.tileID == 3:
                player.x, player.y = self.x, self.y+160
        def update(self):
            self.rect.x = self.x-level.levelPosx+475
            self.rect.y = self.y-level.levelPosy+475
        def draw(self):
            if self.rect.x > -20 and self.rect.x < 960 and self.rect.y > -20 and self.rect.y < 600:
                if self.tileID == 0:
                    if self.y == level.lowestPoint-185:
                        pygame.draw.rect(win, BLACK, pygame.Rect(self.rect.x, self.rect.y, 20, 600-self.rect.y))
                    else:
                        pygame.draw.rect(win, BLACK, self.rect)
                elif self.tileID == 1:
                    pygame.draw.rect(win, RED, self.rect)
                elif self.tileID == 2:
                    pygame.draw.rect(win, PURPLE, self.rect)
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
                
        def checkCollision(self, collider):
            collided = self.rect.colliderect(collider.charRect)
            if collided:
                if self.tileID == 4:
                    player.yVel = -20
                    player.xVel = 0
                if self.tileID == 8:
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
            return collided
        def checkCollisionRect(self, collider):
            return self.rect.colliderect(collider)
            
    
    def redrawScreen():
         
        win.fill(WHITE)
        
        #spikes.draw() 

        for tile in level.levels:
            tile.draw()

        player.draw()


        pygame.draw.rect(win, WHITE, pygame.Rect(0,0, 65, 25))
        win.blit(smallFont.render("FPS: " + str(int(clock.get_fps())), True, (0, 0, 0)), (0,0))
        pygame.draw.rect(win, WHITE, pygame.Rect(0,30, 120, 25))
        win.blit(smallFont.render("YVEL: " + str(player.yVel), True, (0, 0, 0)), (0,30))

        window.blit(pygame.transform.scale(win, (w, h)), (0,0))    
        pygame.display.flip()
    
    speed = 3
    player = Player()
    level = Level()
    semiLevel = SemiLevel()
    #spikes = SpikeLevel()

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

        if ((keys[pygame.K_a] or keys[pygame.K_LEFT]) and not (keys[pygame.K_d] or keys[pygame.K_RIGHT])) or ((keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not (keys[pygame.K_a] or keys[pygame.K_LEFT])):
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                player.changeXVel(speed/10, False)
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not (keys[pygame.K_a] or keys[pygame.K_LEFT]):
                player.changeXVel(speed/10, True)
        elif player.xVel > 0:
            player.xVel-=player.decelSpeed
            player.changeXVel(0, True)
            player.boostDirection = 0
        elif player.xVel < 0:
            player.xVel+=player.decelSpeed
            player.changeXVel(0, False)
            player.boostDirection = 0
            player.canBoost = True
        
        # if not player.climbedLastFrame and player.kTime < 8:
        #     if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and not stompHeld:
        #         player.stomp = True
        #         player.yVel = 20
        #         stompHeld = True
    
        if keys[pygame.K_r]:
            if keys[pygame.K_LCTRL]:
                level.changeLevel()
                player.reset()
                w, h = 960, 600
                window = pygame.display.set_mode((960, 600), pygame.RESIZABLE)
            else:
                player.reset()
        
        
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
        
        
        for tile in level.levels:
            tile.update()
            

        #redraw win
        redrawScreen()
        await asyncio.sleep(0)
        # Set the framerate
        deltaTime = clock.tick(60)/10

asyncio.run(main())
