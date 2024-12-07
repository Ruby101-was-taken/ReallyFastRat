import pygame
from entity import Entity


class AlarmProjectile(Entity):
    def __init__(self, x, y, w, h, image, args={"xVel": 0, "yVel": 0}) -> None:
        super().__init__(x, y, w, h, image, args)
        self.timer = 120
    def start(self):
        self.xVel = self.args["xVel"]
        self.yVel = self.args["yVel"]
        
        return super().start()
    
    def reset(self):
        self.destroy()
        return False
    
    def update(self):
        self.x+=self.xVel
        self.y-=self.yVel
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

    def draw(self, win, showHitBoxes=False):
        return super().draw(win, showHitBoxes)
    

class AlarmProjectileLauncher(Entity):
    def __init__(self, x, y, w, h, image, args=...) -> None:
        super().__init__(x, y, w, h, image, args)
    
    def shoot(self):
        self.trigger.shoot(self.x, self.y)