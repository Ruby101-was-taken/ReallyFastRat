import pygame
from resources import *
from colours import *

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
        if self.popped and self.tileID in [9]:
            if not self in self.level.onScreenLevel:
                self.popped = False

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

        
        if self.popped and self.popTimer>0:
            self.popTimer-=1
            if self.popTimer==0:
                self.popped = False
            
    def checkCollision(self, collider):
        collided = self.rect.colliderect(collider)
        if collided and collider == self.player.charRect and not self.popped:
            # if not self.popped:
            #     self.player.homeTo = (0,0)
            self.player.canHomingAttck = True
            if self.tileID == 4:
                self.player.yVel = -20
                self.player.xVel = 0
            elif self.tileID == 8:
                self.player.yVel = 20
                self.player.xVel = 0
            elif self.tileID == 6:
                self.player.yVel = -13
                self.player.xVel = 0
            elif self.tileID == 2:
                self.player.die()
            elif self.tileID == 5:
                if self.player.yVel > 0:
                    self.player.yVel = 0
                self.player.maxBoost = 20
                self.player.xVel = 13
            elif self.tileID == 7:
                if self.player.yVel > 0:
                    self.player.yVel = 0
                self.player.maxBoost = 20
                self.player.xVel = -13
            elif self.tileID == 9:
                self.player.yVel = -10
                self.player.xVel = 0
                self.popped = True
                self.player.homeTo = (0,0)
                self.popTimer = 360
            elif self.tileID == 10:
                self.gameManager.speed = 0
                self.player.xVel=0
                self.player.jumpPower = 17
            elif self.tileID == 11:
                self.player.powerUps.append(PowerUp(0, 240))
                self.popped = True
            elif self.tileID == 12:
                self.gameManager.collectables+=1
                if self.player.superBoostCoolDown>0:
                    self.player.superBoostCoolDown-=2
                self.popped = True
            elif self.tileID == 13:
                self.gameManager.rareCollectables+=1
                if self.player.superBoostCoolDown>0:
                    self.player.superBoostCoolDown=0
                self.popped = True
            elif self.tileID == 14:
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
