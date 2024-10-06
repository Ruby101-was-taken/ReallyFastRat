import pygame


class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.maxX, self.maxY = 0, 0
        self.minX, self.minY = 0, 0
    
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
        self.x, self.y = int(x), int(y)-175
    def lerpTo(self, x, y):
        self.x, self.y = pygame.math.lerp(self.x, x, 0.2), pygame.math.lerp(self.y, y, 0.2)-175
        
    
    def update(self):
        
        if self.x < self.minX:
            self.x = self.minX
        elif self.x > self.maxX:
            self.x = self.maxX
        if self.y < self.minY:
            self.y = self.minY
        elif self.y > self.maxY:
            self.y = self.maxY