import pygame
from resources import *
from colours import *


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
15 = 
16 = 
17 = 

"""


def createTile(x, y, tileID, image=pygame.Surface((0, 0))):
    match tileID:
        case 0:
            return GroundTile(x,y,tileID,image)
        case 1:
            return SemiSolidTile(x,y,tileID,image)
        case 2:
            return SpikeTile(x,y,tileID,image)
        case 4:
            return SpringTile(x,y,tileID, 20, image)
        case 5:
            return BoosterTile(x,y,tileID, 13, image)
        case 6:
            return SpringTile(x,y,tileID, 13, image)
        case 7:
            return BoosterTile(x,y,tileID, -13, image)
        case 8:
            return SpringTile(x,y,tileID, -20, image)
        case 9:
            return Balloon(x,y,tileID, image)
        case 10:
            return Slime(x,y,tileID, image)
        case _:
            return GroundTile(x,y,tileID,image)
#
class Tile:
    def __init__(self, x, y, tileID, image=pygame.Surface((0,0))):
        self.x, self.y = x, y
        self.tileID = tileID
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.image = image
        self.popped = False
        self.toBeDeleted = False
        self.popTimer = 0
        self.hasBeenDrawn = self.tileID in [9] #this list is the tiles that draw on the fly rather than being static
    def update(self):
        self.rect.x = self.x-self.level.levelPosx+475
        self.rect.y = self.y-self.level.levelPosy+475
        if self.toBeDeleted:
            self.level.levels.remove(self)

        if not self.hasBeenDrawn:
            self.levelDraw()
            self.hasBeenDrawn = True
            
        

        
    def isInSpace(self, x, y):
        return self.x == x and self.y == y
    def reload(self):
        self.popped = False
        
    def levelDraw(self):
        self.level.levelVis.blit(self.image, (self.x, self.y))
    
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

        
            
    def playerCollision(self) -> None:
        pass
    
    def checkCollision(self, collider):
        collided = self.rect.colliderect(collider)
        if collided and collider == self.player.charRect and not self.popped:
            self.playerCollision()
            # if not self.popped:
            #     self.player.homeTo = (0,0)
            self.player.canHomingAttck = True
                
                
            if self.tileID == 11:
                self.player.powerUps.append(PowerUp(0, 240))
                self.popped = True
            if self.tileID == 12:
              self.gameManager.collectables+=1
              if self.player.superBoostCoolDown>0:
                  self.player.superBoostCoolDown-=2
              self.popped = True
            if self.tileID == 13:
              self.gameManager.rareCollectables+=1
              if self.player.superBoostCoolDown>0:
                  self.player.superBoostCoolDown=0
              self.popped = True
            if self.tileID == 14:
                #self.image = objectImages[7]
                self.player.lastSpawn = (self.x, self.y+160)
                self.popped = True
                self.levelDraw()
              

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
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        
class DynamicTile(Tile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
    
    def draw(self):
        if self.rect.x > -20 and self.rect.x < 960 and self.rect.y > -20 and self.rect.y < 600:
            
            pygame.draw.rect(self.win, BLUE, self.rect)
            #self.level.levelVis.blit(self.image, self.rect)
                

        
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
    
class SpikeTile(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        
    def checkCollision(self, collider):
        return super().checkCollision(collider)
        
    def playerCollision(self):
        self.player.die()
    
class SpringTile(StaticTile):
    def __init__(self, x, y, tileID, power, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        self.power = power
        
    def checkCollision(self, collider):
        return super().checkCollision(collider)
    
    def playerCollision(self):
        self.player.yVel = -self.power
        self.player.xVel = 0
        
class BoosterTile(StaticTile):
    def __init__(self, x, y, tileID, power, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        self.power = power
        
    def checkCollision(self, collider):
        return super().checkCollision(collider)
    
    def playerCollision(self):
        if self.player.yVel > 0:
            self.player.yVel = 0
        self.player.maxBoost = 20
        self.player.xVel = self.power
        
class Slime(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
    
    def playerCollision(self):
        self.gameManager.speed = 0
        self.player.xVel=0
        self.player.jumpPower = 17

class Balloon(DynamicTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        
    def playerCollision(self):
        
        print(self.popped)
        self.player.yVel = -10
        self.player.xVel = 0
        self.popped = True
        self.player.homeTo = (0,0)
        self.popTimer = 360
        
        return super().playerCollision()
    
    def update(self):
        
                
        if self.popped:
            if not self in self.level.onScreenLevel:
                self.popped = False
                
        return super().update()
    
    def draw(self):
        if self.popped and self.popTimer>0:
            self.popTimer-=1
            if self.popTimer==0:
                self.popped = False
                
                
        if not self.popped:
            super().draw()
        
        
    
    
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
