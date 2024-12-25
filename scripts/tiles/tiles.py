import pygame, random
from resources import *
from colours import *
from entity import *
from entities.enemy.AlarmProjectile.AlarmProjectile import AlarmProjectile
from scripts.triangleCollisions import rectTriangleCollision
from scripts.tileComponents import *
from entities.entityList import getEntityList
from object import Object

from generalMaths import *



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
23 - End Goal
24 - Death Plane
25 - Evil Rat Spawner
26 - Dash Refill

"""


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
        
        self.components = {}
        
        self.object:Object = None
    def hasObject(self) -> bool: 
        return not self.object is None
    def updateRect(self):
        self.rect.x = self.x-self.level.levelPosx+475+self.offset[0]
        self.rect.y = self.y-self.level.levelPosy+475+self.offset[1]
    def update(self):
        self.updateRect()
        self.checkDelete()
    def checkDelete(self) -> bool:
        if self.toBeDeleted:
            tilex = int((self.x / 20) / 16) * 16
            tiley = int((self.y / 20) / 16) * 16
            chunk_key = f"{int(tilex)}-{int(tiley)}"
            chunk_tiles = self.level.chunks[chunk_key].tiles
            try:
                chunk_tiles.remove(self)
            except ValueError:
                pass  # Tile not in the chunk, ignore
            return True
        return False
            
            
    def singleUpdate(self, deltaTime):
        for component in self.components:
            self.components[component].update(deltaTime)
        
    
    def addComponent(self, component):
        componentType = type(component)
        self.components[componentType] = component

        
    def isInSpace(self, x, y):
        return self.x == x and self.y == y
    def reload(self):
        self.popped = False
        
    def levelDraw(self, offset = (0,0)):
        self.hasBeenDrawn = True
        self.level.levelVis.blit(self.image, (self.x+offset[0], self.y+offset[1]))
        
    def levelDelete(self):
        for y in range(20):
            for x in range(20):
                self.level.levelVis.set_at((self.x+x+self.offset[0], self.y+y+self.offset[1]), (0, 0, 0, 0))
    
    def draw(self, win):
        pass
    
    

        
            
    def playerCollision(self, collider) -> None:
        for component in self.components:
            self.components[component].playerCollision()
    
    def start(self) -> None:
        for component in self.components:
            self.components[component].start()
    
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
    
    def draw(self, win):
        if not self.popped and not self.hasBeenDrawn:
            self.levelDraw()
            self.hasBeenDrawn = True
    def levelDraw(self, offset=(0, 0)):
        self.level.levelInteract.blit(self.image, (self.x+offset[0], self.y+offset[1]))
        
    def levelDelete(self):
        for y in range(20):
            for x in range(20):
                self.level.levelInteract.set_at((self.x+x, self.y+y), (0, 0, 0, 0))
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
        
    def draw(self, win):
        self.levelDelete()
        self.levelDraw(self.offset)
        
        
        
                
        
    def singleUpdate(self, deltaTime):
        
        x = self.x+self.offset[0]
        
        self.levelDelete()
        
        
        
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

        self.levelDraw(self.offset)
    
class SpikeTile(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        self.offset = (1, 1)
        self.rect = pygame.Rect(self.x, self.y, 18, 18)
        
    def checkCollision(self, collider):
        return super().checkCollision(collider)
        
    def playerCollision(self, collider):
        self.player.die()
        
    
class DeathPlane(SpikeTile):
    def __init__(self, x, y, tileID):
        super().__init__(x, y, tileID)
    
class SpringTile(StaticTile):
    def __init__(self, x, y, tileID, power, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        self.power = power
    def start(self):
        if self.object != None:
            self.addComponent(VerticalBounceComponent(self, self.object.getProperty("power")))
            self.addComponent(HorizontalBoost(self, self.object.getProperty("push")))
        else:
            self.addComponent(VerticalBounceComponent(self, self.power))
        return super().start()
    def playerCollision(self, collider):
        self.player.x = self.level.levelPosx = self.x
        self.player.y = self.level.levelPosy = self.y+145
        return super().playerCollision(collider)
        
    
        
class BoosterTile(StaticTile):
    def __init__(self, x, y, tileID, power, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        self.power = power
    def start(self):
        if not self.hasObject():
            self.addComponent(HorizontalBoost(self, self.power))
        else:
            self.addComponent(HorizontalBoost(self, self.object.getProperty("power") * sign(self.power)))
        return super().start()
        
    
        
class Slime(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
    
    def playerCollision(self, collider):
        self.player.xVel = 20
        self.player.lockMovement = True
        return super().playerCollision(collider)

class Balloon(DynamicTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        self.addComponent(CustomRectSize(self, 40, 40))
        
    def playerCollision(self, collider):
        
        self.player.yVel = -10
        self.popped = True
        self.player.homeTo = (0,0)
        self.popTimer = 360
        self.player.x = self.level.levelPosx = self.x
        self.player.y = self.level.levelPosy = self.y+145
        
        self.levelDelete()
        
        return super().playerCollision(collider)
    
    def start(self):
        self.levelDraw()
        if self.hasObject():
            if self.object.hasProperty("time"):
                self.addComponent(RespawnAfter(self, self.object.getProperty("time")))
    
    def update(self):
        
                
        return super().update()
    
    def draw(self, win):
        if self.popped and self.popTimer>0:
            self.popTimer-=1
            if self.popTimer==0:
                self.popped = False
        
        super().draw(win)
                
                
class Coin(DynamicTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        
    def playerCollision(self, collider):
        
        self.gameManager.collectables+=1
        self.gameManager.getCoin()
        if self.player.superBoostCoolDownCoins > self.player.minCoinCoolDown:
            self.player.superBoostCoolDownCoins-=self.player.maxBoostCoolDown/5
            if self.player.superBoostCoolDownCoins < self.player.minCoinCoolDown:
                self.player.superBoostCoolDownCoins = self.player.minCoinCoolDown
        self.popped = True
        
        self.levelDelete()
        
        
        return super().playerCollision(collider)
     
class SuperCoin(DynamicTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        
    def playerCollision(self, collider):
        
        self.gameManager.collectables+=5
        if self.player.superBoostCoolDownCoins > self.player.minCoinCoolDown:
            self.player.superBoostCoolDownCoins-=self.player.maxBoostCoolDown
            if self.player.superBoostCoolDownCoins < self.player.minCoinCoolDown:
                self.player.superBoostCoolDownCoins = self.player.minCoinCoolDown
        self.popped = True
        self.levelDelete()
        
        return super().playerCollision(collider)  
    
class DashRefill(Tile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        
    def playerCollision(self, collider):
        
        self.gameManager.rareCollectables+=1
        if self.player.superBoostCoolDown>0:
            self.player.superBoostCoolDown=0
        
        return super().playerCollision(collider)
    


class Checkpoint(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0)), offset=(0,-100)):
        super().__init__(x, y, tileID, image, offset)
        self.addComponent(CustomRectSize(self, 100, 120, False))
        
    def playerCollision(self, collider) -> None:

        self.player.lastSpawn = (self.x, self.y+160)
        self.popped = True
        
        self.image = tileImages.objectImages[7]
        self.levelDraw()
    
    def reload(self):
        self.image = tileImages.objectImages[6]
        self.levelDraw()
        return super().reload()
    
    
       
class BgTile(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0)), offset=(0, 0)):
        super().__init__(x, y, tileID, image, offset)
        self.toBeDeleted = True
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

    def playerCollision(self, collider) -> None:
        self.points = [(self.rect.x+20, self.rect.y+20), (self.rect.x, self.rect.y+20), (self.rect.x+20, self.rect.y)]
        collided = rectTriangleCollision(collider, self.points)
        
        
        return collided 
    
class Ramp(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0)), offset=(0, 0)):
        super().__init__(x, y, tileID, image, offset)

    def playerCollision(self, collider) -> None:
        self.points = [(self.rect.x+20, self.rect.y+20), (self.rect.x, self.rect.y+20), (self.rect.x+20, self.rect.y)]
        collided = rectTriangleCollision(collider, self.points)
        
        if not self.player.stomp:
            self.player.yVel = min(-3, -self.player.xVel)
            self.player.xVel = max(8, self.player.xVel)
            
        else:
            self.player.yVel = 13
            self.player.xVel = 13
            self.player.stomp = False
        return collided
    

        
        
    
class EndGoal(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, image)
        
    def checkCollision(self, collider):
        return super().checkCollision(collider)
        
    def playerCollision(self, collider):
        self.level.moveLevel()
            
  
class Spawner(StaticTile):
    def __init__(self, x, y, tileID, entityType, w, h, args = {}, entityImage = pygame.Surface((0, 0))):
        super().__init__(x, y, tileID)
        self.entityType  = entityType
        self.w = w
        self.h = h
        self.entityImage = entityImage
        self.args = args
        
        
        
    def start(self) -> None:
        if self.object.hasProperty("entity"):
            self.entityType = getEntityList()[self.object.getProperty("entity")]
        
        self.addComponent(SpawnEntity(self))
        
        super().start()
    
    def spawn(self):
        self.components[SpawnEntity].spawn()
        

class InstantSpawner(Spawner):
    def __init__(self, x, y, tileID, entityType, w, h, args={}, entityImage=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, entityType, w, h, args, entityImage)
        
    def start(self) -> None:
        self.toBeDeleted = True
        super().start()
        self.spawn()
        
class SpawnOnInterval(Spawner):
    def __init__(self, x, y, tileID, entityType, w, h, args={}, entityImage=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, entityType, w, h, args, entityImage)
    def start(self):
        self.interval = self.object.getProperty("interval")
        
        self.entityType = getEntityList()[self.object.getProperty("entity")]
        
        self.addComponent(SpawnerOnInterval(self, self.interval))
    

class EvilRatSpawner(InstantSpawner):
    def __init__(self, x, y, tileID):
        super().__init__(x, y, tileID, EvilRat, 20, 30, {}, resources.entityImages["evilRat"][0])
        

class ToggleBlock(DynamicTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0)), offset=(0, 0), state = True, toggledImage = pygame.Surface((0,0))):
        super().__init__(x, y, tileID, image, offset)
        self.state = state
        self.toggledImage = toggledImage
    def playerCollision(self, collider) -> bool:
        return self.popped
    def update(self):
        self.popped = self.state == self.level.toggleBlockState
    
        return super().update()
    
    def levelDraw(self, offset=(0, 0)):
        if self.state:
            self.level.levelToggleON.blit(self.image, (self.x+offset[0], self.y+offset[1]))
            self.level.levelToggleOFF.blit(self.toggledImage, (self.x+offset[0], self.y+offset[1]))
        else:
            self.level.levelToggleOFF.blit(self.image, (self.x+offset[0], self.y+offset[1]))
            self.level.levelToggleON.blit(self.toggledImage, (self.x+offset[0], self.y+offset[1]))
            
class ToggleSwitch(DynamicTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0)), offset=(0, 0), state = True):
        super().__init__(x, y, tileID, image, offset)
        self.state = state
    def playerCollision(self, collider) -> bool:
        if not self.popped:
            self.level.toggleBlockState = self.state
        return self.popped
    def update(self):
        self.popped = self.state == self.level.toggleBlockState
    
        return super().update()
    
    def levelDraw(self, offset=(0, 0)):
        if self.state:
            self.level.levelToggleOFF.blit(self.image, (self.x+offset[0], self.y+offset[1]))
        else:
            self.level.levelToggleON.blit(self.image, (self.x+offset[0], self.y+offset[1]))
        
    
class ScrollStop(StaticTile):
    def __init__(self, x, y, tileID, stopPos, image=pygame.Surface((0, 0)), offset=(0, 0)):
        super().__init__(x, y, tileID, image, offset)
        self.stopPos = stopPos
    
class StopLessThanX(ScrollStop):
    def __init__(self, x, y, tileID, stopPos, image=pygame.Surface((0, 0)), offset=(0, 0)):
        super().__init__(x, y, tileID, stopPos, image, offset)
        
    def singleUpdate(self, deltaTime):
        if self.player.x < self.x:
            if self.gameManager.camera.y < self.y < self.gameManager.camera.y + 720:
                self.gameManager.camera.setMaxX(self.x-1280)#
                return True
        return False
    
class StopMoreThanX(ScrollStop):
    def __init__(self, x, y, tileID, stopPos, image=pygame.Surface((0, 0)), offset=(0, 0)):
        super().__init__(x, y, tileID, stopPos, image, offset)
        
    def singleUpdate(self, deltaTime):
        if self.player.x > self.x:
            if self.gameManager.camera.y < self.y < self.gameManager.camera.y + 720:
                self.gameManager.camera.setMinX(self.x)
                return True
        return False
    
class StopLessThanY(ScrollStop):
    def __init__(self, x, y, tileID, stopPos, image=pygame.Surface((0, 0)), offset=(0, 0)):
        super().__init__(x, y, tileID, stopPos, image, offset)
        
    def singleUpdate(self, deltaTime):
        if self.player.y-175 < self.y:
            if self.gameManager.camera.x < self.x < self.gameManager.camera.x + 1280:
                self.gameManager.camera.setMaxY(self.y-720)
                return True
        return False
    
class StopMoreThanY(ScrollStop):
    def __init__(self, x, y, tileID, stopPos, image=pygame.Surface((0, 0)), offset=(0, 0)):
        super().__init__(x, y, tileID, stopPos, image, offset)
        
    def singleUpdate(self, deltaTime):
        if self.player.y-175 > self.y:
            if self.gameManager.camera.x < self.x < self.gameManager.camera.x + 1280:
                self.gameManager.camera.setMinY(self.y)
                return True
        return False

class Alarm(Spawner):
    def __init__(self, x, y, tileID, w, h, args={}, entityImage=pygame.Surface((0, 0))):
        super().__init__(x, y, tileID, AlarmProjectile, w, h, args, entityImage)
        
    def playerCollision(self, collider) -> None:
        self.popped = True
        self.shoot()
        return super().playerCollision(collider)

    def shoot(self):
        for ID in self.shootPositions:
            obj = self.level.objects[ID]
            args = {"xVel": obj.customProperties["properties"][0]["value"], "yVel": obj.customProperties["properties"][1]["value"]}
            entity = AlarmProjectile(obj.x, obj.y+177 + self.level.tileHightOffset, self.w, self.h, self.entityImage, args)
            self.chunk.entities.append(entity)
            
            self.setParams(entity)
        
    def update(self):
        return super().update()
    
    def start(self):
        self.shootPositions = []
        
        for prop in self.object.customProperties["properties"]:
            self.shootPositions.append(prop["value"])
        
        return super().start()
        
    # def spawn
        



class LevelChange(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0)), offset=(0, -80)):
        super().__init__(x, y, tileID, image, offset)
        self.rect = pygame.Rect(self.x, self.y, 100, 100)
        
    def start(self):
        self.worldX = self.object.customProperties["properties"][0]["value"]
        self.worldY = self.object.customProperties["properties"][1]["value"]
        return super().start()
        
    def playerCollision(self, collider):
        self.gameManager.goToLevel(self.worldX, self.worldY)
        return super().playerCollision(collider)






class CannotMove(StaticTile):
    def __init__(self, x, y, tileID, image=pygame.Surface((0, 0)), offset=(0, 0)):
        super().__init__(x, y, tileID, image, offset)
    def playerCollision(self, collider):
        self.player.lockMovement = True
        return super().playerCollision(collider)





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


