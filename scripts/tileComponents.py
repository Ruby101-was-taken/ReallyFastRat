
import pygame

class TileComponent:
    def __init__(self, tile):
        self.tile = tile
    def start(self):
        pass
    def update(self, deltaTime):
        pass
    def remove(self):
        self.tile.components.pop(type(self))
    def playerCollision(self):
        pass


class VerticalBounceComponent(TileComponent):
    def __init__(self, tile, power):
        super().__init__(tile)
        self.power = power
    def playerCollision(self):
        self.tile.player.bounce = True
        self.tile.player.yVel = -self.power
        self.tile.player.xVel = 0
        self.tile.player.stomp = False
        self.tile.player.kTime = 0
        
        return super().playerCollision()
    
class HorizontalBoost(TileComponent):
    def __init__(self, tile, power):
        super().__init__(tile)
        self.power = power
    def playerCollision(self):
        if self.tile.player.yVel > 0:
            self.tile.player.yVel = 0
        self.tile.player.maxBoost = 20
        self.tile.player.xVel = self.power
        self.tile.player.stomp = False
        
        return super().playerCollision()
    
class RespawnAfter(TileComponent):
    def __init__(self, tile, time):
        super().__init__(tile)
        self.defaultTime = time
        self.time = self.defaultTime
    def update(self, deltaTime):
        if self.tile.popped:
            self.time-=deltaTime
            if self.time<=0:
                self.time = self.defaultTime
                self.tile.reload()
        return super().update(deltaTime)
    

class CustomRectSize(TileComponent):
    def __init__(self, tile, w, h, centerTile:bool = True):
        super().__init__(tile)
        self.tile.rect = pygame.Rect(self.tile.x, self.tile.y, w, h)
        if centerTile:
            self.tile.offset = ((w/2)-10, (h/2)-10)
        
        
class SpawnEntity(TileComponent):
    def __init__(self, tile):
        super().__init__(tile)
    
    def spawn(self):
        self.tile.chunk.entities.append(self.entityType(self.tile.x, self.tile.y+177, self.tile.w, self.tile.h, self.tile.entityImage, self.tile.args))
        self.setParams()
        
    def setParams(self, entity=None):
        if entity is None:
            entity = self.tile.chunk.entities[-1]
        entity.level = self.tile.level
        entity.gameManager = self.tile.gameManager
        entity.player = self.tile.player
        entity.chunk = self.tile.chunk
        entity.trigger = self.tile
        
        entity.start()
        
class SpawnerOnInterval(SpawnEntity):
    def __init__(self, tile, interval:int):
        super().__init__(tile)
        self.time:float = 0
        self.interval:int = interval
    def update(self, deltaTime):
        self.time+=deltaTime
        if self.time > self.interval:
            self.spawn()
        return super().update(deltaTime)