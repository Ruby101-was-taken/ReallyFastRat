import pygame
from animation import Animation
from resources import *
from colours import *
from profiler import *

class UICanvas:
    def __init__(self, canScroll=False, audioPlayer = None, inputs=None) -> None:
        self.UIComponents = {}
        self.show = True
        self.canScroll = canScroll
        self.scrollPos = 0
        self.audioPlayer = audioPlayer
        self.input = inputs
    def addElement(self, element):
        self.UIComponents[element.tag] = element
        self.UIComponents[element.tag].canvas = self
        self.UIComponents[element.tag].input = self.input
    def getElementByTag(self, tag:str):
        return self.UIComponents[tag]
    def draw(self, win):
        if self.show:
            for element in self.UIComponents:
                self.UIComponents[element].draw(win)
    def update(self):
        if self.canScroll: 
            self.scrollPos += self.input.scrolly*20
            if self.scrollPos > 0: self.scrollPos = 0
            
        if self.show:
            for element in self.UIComponents:
                self.UIComponents[element].update()
                
    def resetScroll(self):
        self.scrollPos = 0
    
    def playClick(self):
        self.audioPlayer.playSound(sounds["click"])
        


class UIElement:
    def __init__(self, screenPos, tag:str, hasShadow=False, shadowOffset=0, shadowColour=(255,255,255), lockScroll = False) -> None:
        self.startPos = screenPos
        self.pos = screenPos
        self.screenPos = screenPos
        
        self.tag = tag
        self.surface = pygame.Surface((0,0), pygame.SRCALPHA)
        self.show = True
        self.hasShadow = hasShadow
        self.shadowOffset = shadowOffset
        self.shadowColour = shadowColour
        self.lockScroll = lockScroll
        
        self.lerp = False
    def toggleShow(self):
        self.show = not self.show
    def setShow(self, setTo:bool):
        self.show = setTo
    def moveTo(self, newPos):
        self.screenPos = newPos
    def draw(self, surf,padding=(0,0),screenPos=None, blitSurf=None, drawShadow=True):
        screenPosWasNone = screenPos==None
        if screenPos==None:
            screenPos = self.screenPos
        if blitSurf==None:
            blitSurf = self.surface
        if self.show:
            surf.blit(blitSurf, (int(screenPos[0]+padding[0]), screenPos[1]+padding[1]))
    def update(self):
        if not self.lockScroll:
            self.screenPos = (self.pos[0], self.pos[1] + self.canvas.scrollPos)
            
        if self.lerp:
            self.pos = self.doLerp()
            self.lerp = self.pos != self.lerpTo
            
    def startLerp(self, to, weight = 1):
        self.lerp = True
        self.lerpWeight = weight
        self.lerpTo = to
            
    def doLerp(self) -> tuple:
        return (int(pygame.math.lerp(self.pos[0], self.lerpTo[0], self.lerpWeight)), int(pygame.math.lerp(self.pos[1], self.lerpTo[1], self.lerpWeight)))
    
    def resetPosition(self):
        self.pos = self.startPos
        self.screenPos = self.pos
    
class UIImage(UIElement):
    def __init__(self, screenPos, tag: str, images=[], fps=1, hasShadow=False, shadowOffset=0, shadowColour=(255, 255, 255), lockScroll = False) -> None:
        super().__init__(screenPos, tag, hasShadow, shadowOffset, shadowColour, lockScroll)
        self.animation = Animation(images, fps)
    def draw(self, surf, padding=(0, 0), screenPos=None, blitSurf=None, drawShadow=True):
        self.surface = self.animation.getFrame()
        return super().draw(surf, padding, screenPos, blitSurf, drawShadow)
    def changeImages(self, images=[], fps=1):
        self.animation = Animation(images, fps)

class UIText(UIElement):
    def __init__(self, screenPos, tag:str, text="", fontSize=10, colour=(0,0,0), padding=20, lockScroll = False) -> None:
        super().__init__(screenPos, tag, lockScroll)
        self.text = text
        self.fontSize = fontSize
        self.colour = colour
        self.font = pygame.font.SysFont("arial", self.fontSize)
        self.padding = padding

        self.setBG(CLEAR)

        self.updateText(text)
    #@profile
    def updateText(self, newText: str, fontSize=None, colour=None):
        # Update font size and colour if provided
        if fontSize is not None and fontSize != self.fontSize:
            self.fontSize = fontSize
            self.font = pygame.font.SysFont("arial", self.fontSize)
        elif not hasattr(self, 'font'):
            self.font = pygame.font.SysFont("arial", self.fontSize)

        if colour is not None:
            self.colour = colour

        # Render text surface
        textSurface = self.font.render(newText, True, self.colour)

        # Calculate the new surface size including padding
        newWidth = textSurface.get_width() + self.padding * 2
        newHeight = textSurface.get_height() + self.padding * 2

        # Only recreate the surface if the size has changed
        if not hasattr(self, 'surface') or self.surface.get_width() != newWidth or self.surface.get_height() != newHeight:
            self.surface = pygame.Surface((newWidth, newHeight), pygame.SRCALPHA)

        # Clear the surface
        self.surface.fill((0, 0, 0, 0))  # Fill with transparent color

        # Update background if necessary
        if self.bg.tag != "textBGEmpty" and (self.bg.surface.get_width() != newWidth or self.bg.surface.get_height() != newHeight):
            self.bg.updateSize(newWidth, newHeight)
            self.bg.updateSurface()

        # Blit background and text surfaces
        self.surface.blit(self.bg.surface, (0, 0))
        self.surface.blit(textSurface, (self.padding, self.padding))

        
    def setBG(self, colour):
        self.bg = UIRect((0,0), "textBG", self.surface.get_width(),self.surface.get_height(), colour)
        self.updateText(self.text)
    def removeBG(self):
        self.bg.tag = "textBGEmpty"
        self.updateText(self.text)
    def updatePadding(self, newPadding):
        self.padding = newPadding
        self.updateText(self.text)

class UIRect(UIElement):
    def __init__(self, screenPos, tag:str, w:int, h:int, colour=(0,0,0), lockScroll = False) -> None:
        super().__init__(screenPos, tag, lockScroll)
        self.updateRect(w, h, colour)
    def updateRect(self, w:int, h:int, colour=None):
        self.w, self.h = w, h
        self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
        if colour != None:
            self.colour = colour
        self.surface.fill(colour)
    def updateSurface(self):
        self.surface.fill(self.colour)
    def updateSize(self, w, h):
        self.w, self.h = w, h
        self.surface = pygame.Surface((w if w > 0 else 1, h), pygame.SRCALPHA)
        self.surface.fill(self.colour)
    def updatePos(self, x,y):
        self.screenPos = (x,y)
        
class UIButton(UIText):
    def __init__(self, screenPos, tag:str, onClick, text="", fontSize=10, padding=20, textColour=(0, 0, 0), buttonColours=((255,255,255), (127,127,127), (0,0,0)), canHold=False, lockScroll = False) -> None:
        super().__init__(screenPos, tag, text, fontSize, textColour, padding, lockScroll)
        self.setBG(buttonColours[0])
        self.onClick = onClick
        self.held = False
        self.canHold = canHold
        self.buttonColours = buttonColours
    def update(self):
        tempRect = self.surface.get_rect()
        tempRect.x, tempRect.y = self.screenPos[0], self.screenPos[1]
        if tempRect.collidepoint(self.input.posx, self.input.posy):
            self.setBG(self.buttonColours[1])
            # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if self.input.clicked[0] and not self.input.clickDown[0]:
                self.input.clickDown[0] = True
                self.setBG(self.buttonColours[2])
                if not self.held:
                    self.held = not self.canHold
                    self.canvas.playClick()
                    self.clickAction()
        if not tempRect.collidepoint(self.input.posx, self.input.posy):
            self.setBG(self.buttonColours[0])

        self.held = self.input.clicked[0] or self.canHold

        return super().update()
    
    def clickAction(self):
        self.onClick()



class UILevelSelect(UIButton):
    def __init__(self, screenPos, tag: str, level, lvl=(0,0), text="", fontSize=10, padding=20, textColour=(0, 0, 0), buttonColours=((255, 255, 255), (127, 127, 127), (0, 0, 0)), canHold=False, lockScroll=False) -> None:
        super().__init__(screenPos, tag, None, text, fontSize, padding, textColour, buttonColours, canHold, lockScroll)
        self.lvl = lvl
        self.level = level
    
    def clickAction(self):
        
        self.level.levelInfo["nextLevel"]["x"] = self.lvl[0]
        self.level.levelInfo["nextLevel"]["y"] = self.lvl[1]
        
        self.level.lvlSelectChangeLevel()
        