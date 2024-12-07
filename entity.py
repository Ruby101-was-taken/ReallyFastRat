import pygame
from resources import *


class Entity:
    def __init__(self, x, y, w, h, image, args = {}) -> None:
        self.x = x
        self.y = y
        
        self.startX, self.startY = self.x, self.y

        self.w, self.h = w, h

        self.image = image

        self.imgW, self.imgH = self.image.get_width(), self.image.get_height()
        self.drawOffset = (self.imgW/2 - w/2, self.imgH/2 - h/2)
        self.charRect = pygame.Rect(x, y, w, h)
        
        self.args = args
        
        self.manualDrawOffset = (0,0)
    
    def reset(self):
        self.x, self.y = self.startX, self.startY
        return True
    def start(self): #called when tile spawns entity in
        pass
    
    def checkCollision(self, obj):
        if self.charRect.colliderect(obj.charRect):
            print("owakpoad")
            return self.rectCollision(obj)
    
    def rectCollision(self, obj):
        return True
    
    def update(self):
        self.moveRect()
    def moveRect(self):
        self.charRect.x = self.x-self.level.levelPosx+475
        self.charRect.y = self.y-self.level.levelPosy+288
    def draw(self, win, showHitBoxes = False):
        blitPosX, blitPosY = self.x - self.gameManager.camera.x - 5, self.y - self.gameManager.camera.y - 175
        if -self.w < blitPosX < 1280 and -self.h < blitPosY < 720: 
            if showHitBoxes:
                pygame.draw.rect(win, (255, 255, 255), self.charRect)
            win.blit(self.image, (blitPosX, blitPosY))
        
    
    def destroy(self):
        self.chunk.entities.remove(self)
        del self
        
     
        

class GravityEntity(Entity):
    def __init__(self, x, y, w, h, image, args={}) -> None:
        super().__init__(x, y, w, h, image, args)
        self.kTime = 0
        self.resetPhysicsValues()
    def resetPhysicsValues(self):
        self.yVel = 0
        
        self.terminalVelocity = 17
        
        self.touchGround = True
    
    def reset(self):
        self.resetPhysicsValues()   
        return super().reset()
    
    def update(self):
        self.gravity()
        return super().update()
    
    def checkCeiling(self):
        self.charRect.height = 1
        if self.level.checkCollision(self.charRect, False):
            self.yVel=+1
            while self.level.checkCollision(self.charRect, False):
                self.y+=1
            self.touchGround=False
            self.kTime = 0
            self.charRect.height = 30
            return True
        else:
            self.charRect.height = 30
            return False

        
    def gravity(self):
       self.yVel+=0.1
       self.y+=self.yVel

class EvilRat(GravityEntity):
    def __init__(self, x, y, w, h, image, args={}) -> None:
        super().__init__(x, y, w, h, resources.playerImages[0], args)
        self.jumpPower = 9
        self.manualDrawOffset = (0, -3)
        
        
    def update(self):
        if self.kTime > 0: self.kTime-=1
        if self.gameManager.input.inputEvent("Jump") and self.kTime > 0:
            self.kTime = 0
            self.yVel = -self.jumpPower
        return super().update()
