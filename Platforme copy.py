import pygame, random, asyncio, os, csv

os.system("cls")


# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 216, 0)
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
            self.charRect = pygame.Rect(self.x, self.y, 20, 30)
            self.image = pygame.image.load("player.png")
            self.kTime = 0
            self.climbedLastFrame=False
        def reset(self):
            self.x = 475
            self.y = 0
            self.xVel = 0
            self.yVel = 0
            level.levelPosx, self.charRect.y = self.x, self.y 
            self.kTime = 0                      
        def changeX(self, speed):
            self.x+=speed
            level.levelPosx=self.x
        def changeXVel(self, speed, isRight):
            
            if isRight:
                self.xVel = speed
                for i in range(int(self.xVel*10)):
                    self.x+=0.1
                    
                    level.levelPosx, self.charRect.y = self.x, self.y
            elif not isRight:
                self.xVel = -speed
                for i in range(-int(self.xVel*10)):
                    self.x-=0.1
                    
            self.changeX(self.xVel)
            
            if self.xVel > 0:
                level.levelPosx, self.charRect.y = self.x+0.1, self.y-0.1
                if level.checkCollision():
                    movedUp = False
                    for i in range(10):
                        self.charRect.y-=1
                        if not level.checkCollision() and not movedUp and not (keys[pygame.K_LCTRL] or keys[pygame.K_LSHIFT]):
                            level.levelPosx+=1
                            movedUp = True

                    if not movedUp:
                        self.charRect.y+=10
                        self.xVel=0
                        self.touchGround = level.checkCollision()
                        while self.touchGround:
                            self.x-=0.1
                            level.levelPosx = self.x
                            self.touchGround = level.checkCollision()
                        if (keys[pygame.K_LCTRL] or keys[pygame.K_LSHIFT]):
                            self.yVel= 0
                            self.climbedLastFrame=True
                            if keys[pygame.K_w] or keys[pygame.K_UP]:
                                self.yVel = -3
                                self.charRect.y -= 30
                                level.levelPosx += 1
                                if not level.checkCollision():
                                    self.yVel = -7
                                self.charRect.y += 30
                                level.levelPosx -= 1
                            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                                self.yVel = 3
                        
            if self.xVel < 0:
                level.levelPosx, self.charRect.y = self.x-0.1, self.y-0.1
                if level.checkCollision():
                    movedUp = False
                    for i in range(10):
                        self.charRect.y-=1
                        if not level.checkCollision() and not movedUp:
                            level.levelPosx-=1
                            movedUp = True
                    if not movedUp:
                        self.charRect.y+=10
                        self.xVel=0
                        self.touchGround = level.checkCollision()
                        while self.touchGround:
                            self.x+=0.1
                            level.levelPosx = self.x
                            self.touchGround = level.checkCollision()
                        if (keys[pygame.K_LCTRL] or keys[pygame.K_LSHIFT]):
                            self.yVel= 0
                            self.climbedLastFrame=True
                            if keys[pygame.K_w] or keys[pygame.K_UP]:
                                self.yVel = -3
                                self.charRect.y -= 30
                                level.levelPosx -= 1
                                if not level.checkCollision():
                                    self.yVel = -7
                                self.charRect.y += 30
                                level.levelPosx += 1
                            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                                self.yVel = 3
            
        def gravity(self):
            if self.charRect.y > h:
                self.die()

            for i in range(int(self.yVel*10)):
                self.y+=0.1
                level.levelPosx, self.charRect.y = self.x, self.y
                if level.checkCollision():
                    self.yVel = 0
                    self.y-=0.1
                    self.charRect.y = self.y
            for i in range(-int(self.yVel*10)):
                self.y-=0.1
                level.levelPosx, self.charRect.y = self.x, self.y
                self.checkCeiling()
            if not level.checkCollision():
                self.yVel+=0.5
                self.kTime -= 1
                if self.kTime<0:
                    self.kTime=0
            
            self.charRect.y+=1
            self.touchGround = level.checkCollision()
            self.charRect.y-=1
            while self.touchGround:
                self.charRect.y = self.y+1
                if not level.checkCollision():
                    self.yVel=+1
                    self.y+=1
                    self.charRect.y = self.y
                    self.touchGround=False
                    self.kTime = 0
                else:
                    self.y-=0.1
                    self.charRect.y = self.y
                    self.touchGround = level.checkCollision()
                    self.kTime = defaultKTime

            if semiLevel.checkCollision():
                self.charRect.y-=int(self.yVel)+1
                if not semiLevel.checkCollision():
                    self.charRect.y+=1
                    
                    self.yVel = 0
                    self.touchGround = True
                    toochSemi = self.semied
                    self.semied = True
                    while not toochSemi:
                        self.charRect.y+=1
                        toochSemi = semiLevel.checkCollision()
                else:
                    self.charRect.y+=int(self.yVel)+1
                    if self.semied:
                        self.kTime = defaultKTime
                    self.semied = False
                self.y = self.charRect.y
            elif self.semied and not keys[pygame.K_SPACE]:
                self.kTime = defaultKTime
                self.semied = False
            elif self.semied:
                self.semied = False
        
        def checkCeiling(self):
            self.charRect.y = self.y-1
            self.charRect.height = 1
            if level.checkCollision():
                self.yVel=+1
                self.y+=1
                self.charRect.y = self.y
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
            level.levelPosx, self.charRect.y = self.x, self.y
            if self.x < 0:
                self.x = 0
                
            self.gravity()
                
            #if spikes.checkCollision():
                #self.die()

            
        def jump(self):
            self.charRect.y+=1
            if self.touchGround or self.kTime>0:
                self.yVel = -10
                self.kTime=0
            self.charRect.y-=1
                
        def draw(self):
            #pygame.draw.rect(win, RED, self.charRect)
            win.blit(self.image, (self.charRect.x-5, self.y))
            
        
    class Level:
        def __init__(self):
            self.levelPosx = 0
            self.changeLevel()
        def checkCollision(self, tileToCheck=0):
            collided = False
            for tile in self.levels:
                tile.update()
                if tile.tileID == tileToCheck:
                    if tile.checkCollision(player):
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
                            print(f"X: {x} Y: {y}")
                            self.levels.append(Tile(x*20, y*20, int(tiles[y][x])))
    class SemiLevel:
        def __init__(self):
            pass
        def checkCollision(self, tileToCheck=1):
            collided = False
            if player.yVel >= 0:
                for tile in level.levels:
                    tile.update()
                    if tile.tileID == tileToCheck:
                        if tile.checkCollision(player):
                            collided = True
                            break
            return collided
        def draw(self):
            #win.blit(self.image, (-level.levelPosx+475,0))
            pass
    class SpikeLevel:
        def __init__(self):
            self.image = pygame.image.load(f"levels/spike/{worldX}-{worldY}.png")
            self.mask = pygame.mask.from_surface(self.image)
        def checkCollision(self):
            feetRect = pygame.Rect(level.levelPosx, player.charRect.y+29, 20, 1)
            self.offset = (feetRect.x, feetRect.y)
            self.overlap = self.mask.overlap(pygame.mask.from_surface(pygame.Surface(feetRect.size)), self.offset)

            if self.overlap is not None:
                return True
            else:
                return False

        def draw(self):
            win.blit(self.image, (-level.levelPosx+475,0))
        def changeLevel(self):
            self.image = pygame.image.load(f"levels/spike/{worldX}-{worldY}.png")
            self.mask = pygame.mask.from_surface(self.image)

    class Tile:
        def __init__(self, x, y, tileID):
            self.x, self.y = x, y
            self.tileID = tileID
            print(x,y)
            self.rect = pygame.Rect(self.x, self.y, 20, 20)
        def update(self):
            self.rect.x = self.x-level.levelPosx+475
        def draw(self):
            pygame.draw.rect(win, BLACK, self.rect)
        def checkCollision(self, collider):
            return self.rect.colliderect(collider.charRect)
            
    
    def redrawScreen():
         
        win.fill(WHITE)
        
        player.draw()
        level.draw()    
        semiLevel.draw()  
        #spikes.draw() 
        win.blit(smallFont.render(str(int(clock.get_fps())), True, (0, 0, 0)), (0,0))

        for tile in level.levels:
            tile.draw()

        window.blit(pygame.transform.scale(win, (w, h)), (0,0))     
        pygame.display.flip()
    
    player = Player()
    level = Level()
    semiLevel = SemiLevel()
    #spikes = SpikeLevel()
    speed = 2

    spaceHeld = False
    
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

        
        keys = pygame.key.get_pressed()

        if spaceHeld:
            spaceHeld = keys[pygame.K_SPACE]


        if keys[pygame.K_SPACE] and not spaceHeld:
            player.jump()
            spaceHeld = True
        player.process()
        if keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.changeXVel(speed, False)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.changeXVel(speed, True)
        elif player.xVel > 0:
            player.xVel=0
        elif player.xVel < 0:
            player.xVel=0
    
        if keys[pygame.K_r]:
            if keys[pygame.K_LCTRL]:
                level.changeLevel()
                semiLevel.changeLevel()
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
        clock.tick(60)

asyncio.run(main())
