import pygame
from resources import *
from colours import *

from sign import sign



class TileImages:
    def __init__(self) -> None:
        pass

tileImages = TileImages()

"""

0 = ground
1 = semiSolid
2 = spike
3 = start
4 = bounce up
5 = bounce right
6 = bounce up weak
7 = bounce left
8 = bounce down
9 = homing balloon
10 = slime
11 = jump power up
12 = coin
13 = collectable
14 = checkpoint
15 = ground B (aka just a different looking ground)
16 = ground c
17 = ground d
18 = move up platform
19 = BG Tile
20 = BG Tile
21 = BG Tile
21 = BG Tile
22 - Moving platform

"""


def createTile(x, y, tileID, image=pygame.Surface((0, 0))):
    match tileID:
        case 0:
            return GroundTile(x,y,tileID)
        case 1:
            return SemiSolidTile(x,y,tileID)
        case 2:
            return SpikeTile(x,y,tileID)
        case 4:
            return SpringTile(x,y,tileID, 20)
        case 5:
            return BoosterTile(x,y,tileID, 13)
        case 6:
            return SpringTile(x,y,tileID, 13)
        case 7:
            return BoosterTile(x,y,tileID, -13)
        case 8:
            return SpringTile(x,y,tileID, -20)
        case 9:
            return Balloon(x,y,tileID, tileImages.objectImages[8])
        case 10:
            return Slime(x,y,tileID, image)
        case 12:
            return Coin(x,y,tileID, tileImages.objectImages[9])
        case 13:
            return SuperCoin(x,y,tileID, tileImages.objectImages[10])
        case 14:
            return Checkpoint(x,y,tileID)
        case 15:
            return GroundTile(x,y,tileID)
        case 16:
            return GroundTile(x,y,tileID)
        case 17:
            return GroundTile(x,y,tileID)
        case 18:
            return BgTile(x,y,tileID)
        case 19:
            return BgTile(x,y,tileID)
        case 20:
            return BgTile(x,y,tileID)
        case 21:
            return BgTile(x,y,tileID)
        case 22:
            return MovingPlatform(x,y,tileID, (0,0))
        case _:
            return StaticTile(x,y,tileID)
#
class Tile:
    def __init__(self, x, y, tileID, image=pygame.Surface((0,0)), offset=(0,0)):
        self.x, self.y = x, y
        self.tileID = tileID
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.image = image
        self.popped = False
        self.toBeDeleted = False
        self.popTimer = 0
        self.hasBeenDrawn = False
        self.offset = offset
        
        self.tilePos = (x/20, y/20)
    def update(self):
        self.rect.x = self.x-self.level.levelPosx+475+self.offset[0]
        self.rect.y = self.y-self.level.levelPosy+475+self.offset[1]
        if self.toBeDeleted:
            self.level.levels.remove(self)

        if not self.hasBeenDrawn:
            self.levelDraw()
            self.hasBeenDrawn = True
            
    def singleUpdate(self):
        pass
    

        
    def isInSpace(self, x, y):
        return self.x == x and self.y == y
    def reload(self):
        self.popped = False
        
    def levelDraw(self, offset = (0,0)):
        self.level.levelVis.blit(self.image, (self.x+offset[0], self.y+offset[1]))
        
    def levelDelete(self):
        for y in range(20):
            for x in range(20):
                self.level.levelVis.set_at((self.x+x+self.offset[0], self.y+y+self.offset[1]), (0, 0, 0, 0))
    
    def draw(self):
        if self.rect.x > -20 and self.rect.x < 960 and self.rect.y > -20 and self.rect.y < 600:
            if self.level.quickDraw:
                if self.tileID == 0:
                    if self.y == self.level.lowestPoint-185:
                        pygame.draw.rect(self.win, BLACK, pygame.Rect(self.rect.x, self.rect.y, 20, 600-self.rect.y))
                    else:
                        pygame.draw.rect(self.win, BLACK, self.rect)
                elif self.tileID == 4:
                    pygame.draw.rect(self.win, BLUE, self.rect)
                elif self.tileID == 8:
                    pygame.draw.rect(self.win, GREY, self.rect)
                elif self.tileID == 5:
                    pygame.draw.rect(self.win, GREEN, self.rect)
                elif self.tileID == 6:
                    pygame.draw.rect(self.win, YELLOW, self.rect)
                elif self.tileID == 7:
                    pygame.draw.rect(self.win, BROWN, self.rect)
            elif self.tileID == 9 and not self.popped:
                if self.player.homeTo == (self.x, self.y+160):
                    pygame.draw.rect(self.win, RED, self.rect)
                else:
                    pygame.draw.rect(self.win, CYAN, self.rect)

            elif self.tileID == 12 and not self.popped:
                pygame.draw.rect(self.win, GOLD, self.rect)
            elif self.tileID == 13 and not self.popped:
                pygame.draw.rect(self.win, MAGENTA, self.rect)

        
            
    def playerCollision(self, collider) -> None:
        pass
    
    def start(self) -> None:
        pass
    
    def checkCollision(self, collider):
        collided = self.rect.colliderect(collider)
        if collided and collider == self.player.charRect and not self.popped:
            playerCollideOutcome = self.playerCollision(collider)
            collided = playerCollideOutcome if playerCollideOutcome != None else collided
            # if not self.popped:
            #     self.player.homeTo = (0,0)
            self.player.canHomingAttck = True
                
                
            if self.tileID == 11:
                self.player.powerUps.append(PowerUp(0, 240))
                self.popped = True
              
              

        elif collided and collider == self.player.homingRange and not self.popped:
            if self.tileID == 9:
                self.player.homeTo = (self.x, self.y+160)
                self.player.maxBoost = 20
                self.player.homingCoolDown = 30
                
                if self.level.levelPosx < self.player.homeTo[0]:
                    self.player.homeRight = True
                elif self.level.levelPosx > self.player.homeTo[0]:
                    self.player.homeRight = False
                if self.level.levelPosy < self.player.homeTo[1]:
                    self.player.homeDown = True
                elif self.level.levelPosy > self.player.homeTo[1]:
                    self.player.homeDown = False
        elif collided and collider == self.player.homingRange and self.popped:
            collided = False



                
        return collided
    def checkCollisionRect(self, collider):
        return self.rect.colliderect(collider)
    
    
class StaticTile(Tile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0)), offset=(0,0)):
        super().__init__(x, y, tileID, image, offset)
        
class DynamicTile(Tile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0)), offset=(0,0)):
        super().__init__(x, y, tileID, image, offset)
    
    def draw(self):
        if not self.popped and not self.hasBeenDrawn:
            self.levelDraw()
            self.hasBeenDrawn = True
            
    def levelDraw(self, offset = (0,0)):
        self.level.levelInteract.blit(self.image, (self.x+offset[0], self.y+offset[1]))
        
    def levelDelete(self):
        for y in range(20):
            for x in range(20):
                self.level.levelInteract.set_at((self.x+x+self.offset[0], self.y+y+self.offset[1]), (0, 0, 0, 0))
    
    def reload(self):
        self.levelDraw()
        return super().reload()
    


                

        
class GroundTile(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        
    def checkCollision(self, collider):
        return super().checkCollision(collider)
    
class SemiSolidTile(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        
    def checkCollision(self, collider):
        return super().checkCollision(collider)
    
    
    
    

class MovingPlatform(DynamicTile):
    def __init__(self, x, y, tileID, offset=(0, 0), moveBy = 80, speed = 1):
        self.moveBy = moveBy
        self.speed = speed
        self.startX, self.startY = x, y
        self.moveOut = True
        
        self.xVel, self.yVel = 0, 0
        
        super().__init__(x, y, tileID, pygame.Surface((0, 0)), offset)
    
    def start(self):
        self.levelDelete()
        
    def draw(self):
        self.levelDelete()
        self.levelDraw(self.offset)
        
        
        
                
        
    def singleUpdate(self):
        
        x = self.x+self.offset[0]
        
        
        if self.moveOut:
            if x < self.startX+self.moveBy:
                self.offset = (self.offset[0] + self.speed, self.offset[1])
                self.xVel = self.speed
            else: 
                self.offset = (self.startX+self.moveBy, self.offset[1])
                self.xVel = 0
            
            x = self.x+self.offset[0]
            
            self.moveOut = (x < self.startX+self.moveBy)
            
        else:
            if x > self.startX:
                self.offset = (self.offset[0] - self.speed, self.offset[1])
                self.xVel = -self.speed
            else: 
                self.offset = (0, self.offset[1])
                self.xVel = 0
            
            x = self.x+self.offset[0]
            
            self.moveOut = (self.offset[0] == 0)

    
    
    
class SpikeTile(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        
    def checkCollision(self, collider):
        return super().checkCollision(collider)
        
    def playerCollision(self, collider):
        self.player.die()
    
class SpringTile(StaticTile):
    def __init__(self, x, y, tileID, power, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        self.power = power
        
    def checkCollision(self, collider):
        return super().checkCollision(collider)
    
    def playerCollision(self, collider):
        self.player.yVel = -self.power
        self.player.xVel = 0
        
class BoosterTile(StaticTile):
    def __init__(self, x, y, tileID, power, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        self.power = power
        
    def checkCollision(self, collider):
        return super().checkCollision(collider)
    
    def playerCollision(self, collider):
        if self.player.yVel > 0:
            self.player.yVel = 0
        self.player.maxBoost = 20
        self.player.xVel = self.power
        
class Slime(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
    
    def playerCollision(self, collider):
        self.gameManager.speed = 0
        self.player.xVel=0
        self.player.jumpPower = 17

class Balloon(DynamicTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        
    def playerCollision(self, collider):
        
        self.player.yVel = -10
        self.player.xVel = 0
        self.popped = True
        self.player.homeTo = (0,0)
        self.popTimer = 360
        
        self.levelDelete()
        
        return super().playerCollision(collider)
    
    def start(self):
        self.levelDraw()
    
    def update(self):
        
                
        if self.popped:
            if not self in self.level.onScreenLevel:
                self.popped = False
                self.hasBeenDrawn = False
                
        return super().update()
    
    def draw(self):
        if self.popped and self.popTimer>0:
            self.popTimer-=1
            if self.popTimer==0:
                self.popped = False
                self.levelDraw()
        
        super().draw()
                
                
class Coin(DynamicTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        
    def playerCollision(self, collider):
        
        self.gameManager.collectables+=1
        if self.player.superBoostCoolDown>0:
            self.player.superBoostCoolDown-=2
        self.popped = True
        
        self.levelDelete()
        
        return super().playerCollision(collider)
     
class SuperCoin(DynamicTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        
    def playerCollision(self, collider):
        
        self.gameManager.rareCollectables+=1
        if self.player.superBoostCoolDown>0:
            self.player.superBoostCoolDown=0
        self.popped = True
        self.levelDelete()
        
        return super().playerCollision(collider)
    


class Checkpoint(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0)), offset=(0,-100)):
        super().__init__(x, y, tileID, image, offset)
        self.rect = pygame.Rect(self.x, self.y, 100, 100)
        
    def playerCollision(self, collider) -> None:

        self.player.lastSpawn = (self.x, self.y+160)
        self.popped = True
        
        self.image = tileImages.objectImages[7]
        self.levelDraw()
    
    def reload(self):
        self.image = tileImages.objectImages[6]
        return super().reload()
    
    
       
class BgTile(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0)), offset=(0, 0)):
        super().__init__(x, y, tileID, image, offset)
    
    def checkCollision(self, collider):
        return False
    
    def levelDraw(self, offset = (0,0)):
        self.level.levelBG.blit(self.image, (self.x+offset[0], self.y+offset[1]))
        
    def levelDelete(self):
        for y in range(self.size):
            for x in range(self.size):
                self.level.levelBG.set_at((self.x+x+self.offset[0], self.y+y+self.offset[1]), (0, 0, 0, 0))

        
class Slope(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0)), offset=(0, 0)):
        super().__init__(x, y, tileID, image, offset)
        self.mask = pygame.mask.from_surface(self.image)

    def playerCollision(self, collider) -> None:
        offset = ((collider.x - self.rect.x), (collider.y - self.rect.y)+10)
        collided = self.mask.overlap(pygame.mask.from_surface(self.player.rectAsSurface), offset) is not None
        
        
        
        return collided
    

        
            
        
        
        
        
class PowerUp:
    def __init__(self, powerType, time = 120):
        self.type = powerType
        self.time = time
    def draw(self, y):
        self.win.blit(pygame.font.SysFont("arial", 20).render(f"powerup: {int(self.time/60)}", True, RED), (850, (y*20)))
        self.player.jumpPower += 6
        self.time-=1
        if self.time <=0:
            self.player.powerUps.remove(self)
