import pygame
from entity import GravityEntity
from resources import resources

class Bubble(GravityEntity):
    def __init__(self, x, y, w, h, image, args={}) -> None:
        super().__init__(x, y, 20, 20, resources.playerImages[0], args)
        
        
    def update(self):
        if self.y > self.startY+300:
            self.destroy()
        
        return super().update()