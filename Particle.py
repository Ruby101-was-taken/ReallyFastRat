import pygame
from colours import *

class Particle:
    def __init__(self, x, y, xVel, yVel, w, h, time, colour) -> None:
        self.x, self.y = x, y
        self.xVel, self.yVel = xVel, yVel
        
        self.w, self.h = w, h
        self.colour = colour
        
        self.time = time
        
        self.surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.surf.fill(self.colour)
        
    def draw(self, win, deltaTime):
        
        self.x += self.xVel*deltaTime
        self.y += self.yVel*deltaTime
        
        self.time-=deltaTime
        
        
        win.blit(self.surf, (self.x - self.gameManager.camera.x, self.y - self.gameManager.camera.y - 175))
        
        
        if self.time <= 0:
            self.gameManager.particles.remove(self)
    
    def kill(self):
        self.time = 0
        
        
class OnScreenParticle(Particle):
    def __init__(self, x, y, xVel, yVel, w, h, time, colour):
        super().__init__(x, y, xVel, yVel, w, h, time, colour)
        
    def draw(self, win, deltaTime):
        self.x += self.xVel*deltaTime
        self.y += self.yVel*deltaTime
        
        self.time-=deltaTime
        
        
        win.blit(self.surf, (self.x, self.y))
        
        
        if self.time <= 0:
            self.gameManager.particles.remove(self)
        