import pygame
from entity import Entity


class AlarmProjectile(Entity):
    def __init__(self, x, y, w, h, image, args={}) -> None:
        super().__init__(x, y, w, h, image, args)
        self.timer = 120
    def start(self):
        self.xVel = (self.player.x + 200 - self.x)/25
        self.yVel = (self.player.y - self.y)/25
        return super().start()
    
    def reset(self):
        self.destroy()
    
    def update(self):
        self.x+=self.xVel
        self.y-=self.xVel
        self.timer -= 1
        if self.timer <= 0:
            self.destroy()
        return super().update()
    
    def destroy(self):
        self.trigger.popped = False
        return super().destroy()
    
    def rectCollision(self, obj):
        if(obj == self.player):
            self.player.die()
        return super().rectCollision(obj)
    

class AlarmProjectileLauncher(Entity):
    def __init__(self, x, y, w, h, image, args=...) -> None:
        super().__init__(x, y, w, h, image, args)
    
    def shoot(self):
        self.trigger.shoot(self.x, self.y)