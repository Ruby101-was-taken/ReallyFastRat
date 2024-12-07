import pygame


class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.maxX, self.maxY = 0, 0
        self.minX, self.minY = 0, 0
        
        self.levelEdgeMaxX, self.levelEdgeMaxY = 0, 0
        
        self.lerpSpeed = 0.1
        
        
    def setLevelEdgeMaxes(self, x, y):
        self.levelEdgeMaxX = x
        self.levelEdgeMaxY = y
        self.setMaxes(x, y)
    
    def setMaxes(self, x, y):
        self.setMaxX(x)
        self.setMaxY(y)
    def setMaxX(self, x):
        self.maxX = x
    def setMaxY(self, y):
        self.maxY = y
        
    def setMins(self, x, y):
        self.setMinX(x)
        self.setMinY(y)
    def setMinX(self, x):
        self.minX = x
    def setMinY(self, y):
        self.minY = y
        
    def setPos(self, x, y):
        
        setX = True
        setY = True
        
        
        if x < self.minX:
            setX = False
            if self.minX == 0:
                self.x = 0
            else:
                self.x = pygame.math.lerp(self.x, self.minX, self.lerpSpeed)
            
            
        elif x > self.maxX:
            setX = False
            if self.maxX == self.levelEdgeMaxX:
                self.x = self.levelEdgeMaxX
            else:
                self.x = pygame.math.lerp(self.x, self.maxX, self.lerpSpeed)
            
        
        if y-175 < self.minY:
            setY = False
            if self.minY == 0:
                self.y = 0
            else:
                self.y = pygame.math.lerp(self.y, self.minY, self.lerpSpeed)
            
            
        elif y-175 > self.maxY:
            setY = False
            if self.maxY == self.levelEdgeMaxY:
                self.y = self.levelEdgeMaxY
            else:
                self.y = pygame.math.lerp(self.y, self.maxY, self.lerpSpeed)
            
        
        # if self.x < self.minX:
        #     self.x = self.minX
            
        # elif self.x > self.maxX:
        #     self.x = self.maxX
        
        
        
        if setX: self.x = int(x)
        if setY: self.y = int(y)-175
        
            
        
    
    def update(self):
        pass
        
            