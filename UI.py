import pygame
from animation import Animation
from resources import *
from colours import *
from profiler import *


testMap = {
    "start": {"up": "settings", "down": "quit"}
}

class UISTYLE:
    def __init__(self, hasBackground = False, colour=(0,0,0), borderWidth=0, borderRadius = 0, borderColour=(0,0,0), font = "rubfont.ttf", fontSize = 10, fontColour = (255, 255, 255), padding = 20, hasShadow = False, shadowColour = (0,0,0), shadowOffset = 10) -> None:
        self.hasBackground = hasBackground
        self.colour = colour
        self.width = borderWidth
        self.radius = borderRadius
        self.borderColour = borderColour
        
        self.font = pygame.font.Font(f"ui/fonts/{font}", fontSize)
        self.fontName = font
        self.fontSize = fontSize
        self.fontColour = fontColour
        self.padding = padding
        
        self.hasShadow = hasShadow
        self.shadowColour = shadowColour
        self.shadowOffset = shadowOffset
        
class UIBUTTONSTYLE:
    def __init__(self, style, hoverStyle=None, pressedStyle=None):
        if hoverStyle is None:
            hoverStyle = style
        if pressedStyle is None:
            pressedStyle = style
        self.styles = (style, hoverStyle, pressedStyle)

        

class UICanvas:
    def __init__(self, canScroll=False, audioPlayer = None, inputs=None, maxScroll=0) -> None:
        self.UIComponents = {}
        self.show = True
        self.canScroll = canScroll
        self.scrollPos = 0
        self.maxScroll = maxScroll
        self.audioPlayer = audioPlayer
        self.input = inputs

        self.highlightedElement = ""
        self.hasMap = False
        
        self.scrolling = False
        
        self.showHighlight = True
    def makeMap(self, addMap):
        self.hasMap = True
        self.highlightedElement = list(addMap.keys())[0]
        self.UIMap = UIMap()
        
        for currentElement, connections in addMap.items():
            for direction, element in connections.items():
                self.UIMap.createLink(currentElement, element, direction)
                
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
            if self.hasMap and self.showHighlight and not self.input.careForMouse:
                self.getElementByTag(self.highlightedElement).drawHighlight(win)
    def update(self):
        if self.show:
            if self.hasMap:
                if self.showHighlight:
                    self.highlightedElement = self.UIMap.move(self.input, self)
                elif self.input.careForMouse:
                    self.showHighlight = True   
                    
            
                if self.input.inputEvent("UIACCEPT", False) and self.showHighlight:
                    self.showHighlight = True
                    if type(self.getElementByTag(self.highlightedElement)) in [UIButton, UILevelSelect]:
                        self.getElementByTag(self.highlightedElement).press()
                        
                elif self.input.inputEvent("UIBACK", False):
                    self.showHighlight = True
                    if self.UIMap.hasBack():
                        self.getElementByTag("back").press()
                
                
                if self.canScroll and not self.scrolling and not self.input.careForMouse:
                    if self.getElementByTag(self.highlightedElement).pos[1] > 720 - self.scrollPos-120 and not abs(self.scrollPos)==self.maxScroll and not self.getElementByTag(self.highlightedElement).lockScroll:
                        self.scrollPos-=10
                        self.showHighlight = False
                    elif self.getElementByTag(self.highlightedElement).pos[1] < abs(self.scrollPos)+100 and not self.getElementByTag(self.highlightedElement).lockScroll:
                        self.scrollPos+=10
                        self.showHighlight = False
                    else:
                        self.showHighlight = True
                        
            
                
            if self.canScroll and self.input.scrolly!=0: 
                self.scrolling = True
                self.scrollPos += self.input.scrolly*20
                if self.scrollPos > 0: self.scrollPos = 0
            
            if abs(self.scrollPos) > self.maxScroll:
                self.scrollPos = -self.maxScroll
                
            if self.show:
                for element in self.UIComponents:
                    self.UIComponents[element].update()
             
         
    def resetScroll(self):
        self.scrollPos = 0
    
    def playClick(self):
        self.audioPlayer.playSound(sounds["click"])
        


class UIElement:
    def __init__(self, screenPos, tag:str, style = UISTYLE(), lockScroll = False) -> None:
        self.startPos = screenPos
        self.pos = screenPos
        self.screenPos = screenPos
        
        self.tag = tag
        self.surface = pygame.Surface((0,0), pygame.SRCALPHA)
        self.show = True
        
        self.style = style
        
        self.hasShadow = self.style.hasShadow
        self.shadowOffset = self.style.shadowOffset
        self.shadowColour = self.style.shadowColour
        
        self.lockScroll = lockScroll
        
        self.lerp = False
        
        self.updateShadow()
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
        
        if self.style.hasShadow:
            surf.blit(self.shadowSurf, (int(screenPos[0]+padding[0]+self.style.shadowOffset), screenPos[1]+padding[1]+self.style.shadowOffset))
        
        if self.show:
            surf.blit(blitSurf, (int(screenPos[0]+padding[0]), screenPos[1]+padding[1]))
    def updateShadow(self):
        
        if self.style.hasShadow:
            self.shadowSurf = pygame.Surface.copy(self.surface)
            self.shadowSurf.fill(self.style.shadowColour, special_flags=pygame.BLEND_RGBA_MIN)
        
    def drawHighlight(self, surf,padding=(0,0),screenPos=None):
        screenPosWasNone = screenPos==None
        if screenPos==None:
            screenPos = self.screenPos
        if self.show:
            surf.blit(uiAssets["pointer"], (int(screenPos[0]+padding[0])-42, screenPos[1]+padding[1] + (self.bg.h/2)-12))
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
    def __init__(self, screenPos, tag: str, images=[], fps=1, style = UISTYLE(), lockScroll = False) -> None:
        super().__init__(screenPos, tag, style, lockScroll)
        self.animation = Animation(images, fps)
        self.surface = self.animation.getFrame()
        self.updateShadow()
    def draw(self, surf, padding=(0, 0), screenPos=None, blitSurf=None, drawShadow=True):
        self.surface = self.animation.getFrame()
        return super().draw(surf, padding, screenPos, blitSurf, drawShadow)
    def changeImages(self, images=[], fps=1):
        self.animation = Animation(images, fps)
        self.updateShadow()

class UIText(UIElement):
    def __init__(self, screenPos, tag:str, text="", style = UISTYLE(), lockScroll = False) -> None:
        super().__init__(screenPos, tag, style, lockScroll)
        self.text = text

        if not self.style.hasBackground:
            self.setBG(CLEAR)
        else:
            self.setBG(self.style.colour)

        self.updateText(text)
        
    def updateText(self, newText: str, fontSize=None, colour=None):
        # Update font size and colour if provided
        if fontSize is not None and fontSize != self.style.fontSize:
            self.style.fontSize = fontSize
            self.style.font = pygame.font.Font(f"ui/fonts/{self.style.fontName}", self.style.fontSize)
        elif not hasattr(self, 'font'):
            self.style.font = pygame.font.Font(f"ui/fonts/{self.style.fontName}", self.style.fontSize)

        if colour is not None:
            self.style.colour = colour

        # Render text surface
        textSurface = self.style.font.render(newText, True, self.style.fontColour)

        # Calculate the new surface size including padding
        newWidth = textSurface.get_width() + self.style.padding * 2
        newHeight = textSurface.get_height() + self.style.padding * 2

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
        self.surface.blit(textSurface, (self.style.padding, self.style.padding))

        self.updateShadow()
    def setBG(self, colour):
        self.style.colour = colour
        self.bg = UIRect((0,0), "textBG", self.surface.get_width(),self.surface.get_height(), style = self.style)
        self.updateText(self.text)
    def removeBG(self):
        self.bg.tag = "textBGEmpty"
        self.updateText(self.text)
    def updatePadding(self, newPadding):
        self.padding = newPadding
        self.updateText(self.text)

class UIRect(UIElement):
    def __init__(self, screenPos, tag:str, w:int, h:int, lockScroll = False, style = UISTYLE()) -> None:
        super().__init__(screenPos, tag, style, lockScroll)
        self.updateRect(w, h, self.style.colour)
        
    def updateRect(self, w:int, h:int, colour=None):
        self.w, self.h = w, h
        if colour != None:
            self.style.colour = colour
        self.updateSurface()
        self.updateShadow()
    def updateSurface(self):
        self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, self.style.colour, self.rect, 0, self.style.radius)
        if self.style.width > 0:
            pygame.draw.rect(self.surface, self.style.borderColour, self.rect, self.style.width, self.style.radius)
    def updateSize(self, w, h):
        self.w, self.h = w, h
        self.updateSurface()
    def updatePos(self, x,y):
        self.screenPos = (x,y)
        
class UIButton(UIText):
    def __init__(self, screenPos, tag:str, onClick, text="", style=UIBUTTONSTYLE(UISTYLE()), canHold=False, lockScroll = False) -> None:
        super().__init__(screenPos, tag, text, style.styles[0], lockScroll)
        self.styles = style
        self.style = self.styles.styles[0]
        self.setBG(self.style.colour)
        self.onClick = onClick
        self.held = False
        self.canHold = canHold
        self.lastStyle = 0
    def update(self):
        tempRect = self.surface.get_rect()
        tempRect.x, tempRect.y = self.screenPos[0], self.screenPos[1]
        if (tempRect.collidepoint(self.input.posx, self.input.posy) and self.input.careForMouse):
            self.canvas.highlightedElement = self.tag
            if self.lastStyle != 1:
                self.style = self.styles.styles[1]
                self.setBG(self.style.colour)
            self.lastStyle = 1
            
            if self.input.clicked[0] and not self.input.clickDown[0]:
                self.input.clickDown[0] = True
                self.press()
                
        elif self.canvas.highlightedElement == self.tag and self.lastStyle != 1 and not self.input.careForMouse:
            self.style = self.styles.styles[1]
            self.setBG(self.style.colour)
            self.lastStyle = 1
        elif self.canvas.highlightedElement != self.tag or self.input.careForMouse:
            if self.lastStyle!=0:
                self.style = self.styles.styles[0]
                self.setBG(self.style.colour)
                self.lastStyle = 0

        self.held = self.input.clicked[0] or self.canHold

        return super().update()
    
    def press(self):
        self.canvas.scrolling = True
        self.style = self.styles.styles[2]
        self.setBG(self.style.colour)
        self.lastStyle = 2
        if not self.held:
            self.held = not self.canHold
            self.canvas.playClick()
            self.clickAction()
    
    def clickAction(self):
        self.onClick()
        
        
    
        



class UILevelSelect(UIButton):
    def __init__(self, screenPos, tag: str, level, lvl=(0,0), text="", style=UISTYLE(), buttonColours=((255, 255, 255), (127, 127, 127), (0, 0, 0)), canHold=False, lockScroll=False) -> None:
        super().__init__(screenPos, tag, None, text, style, buttonColours, canHold, lockScroll)
        self.lvl = lvl
        self.level = level
    
    def clickAction(self):
        
        self.level.levelInfo["nextLevel"]["x"] = self.lvl[0]
        self.level.levelInfo["nextLevel"]["y"] = self.lvl[1]
        
        self.level.lvlSelectChangeLevel()
        
        
        
class UIMap:
    def __init__(self) -> None:
        self.links = {}
        
    def createLink(self, start, end, direction):
        if start not in self.links:
            self.links[start] = {}
        self.links[start][direction] = end
        
    def hasBack(self) -> bool:
        return "back" in self.links
    
    def successfulMove(self, canvas):
        canvas.audioPlayer.playSound(sounds["menuMove"])
        canvas.scrolling = False
        
    def move(self, inputs, canvas):
        caredForMouse = inputs.careForMouse
        if inputs.inputEvent("UIUP", False):
            if "up" in self.links[canvas.highlightedElement]:
                self.successfulMove(canvas)
                return self.links[canvas.highlightedElement]["up"] if not caredForMouse else canvas.highlightedElement
        elif inputs.inputEvent("UIDOWN", False):
            if "down" in self.links[canvas.highlightedElement]:
                self.successfulMove(canvas)
                return self.links[canvas.highlightedElement]["down"] if not caredForMouse else canvas.highlightedElement
        elif inputs.inputEvent("UILEFT", False):
            if "left" in self.links[canvas.highlightedElement]:
                self.successfulMove(canvas)
                return self.links[canvas.highlightedElement]["left"] if not caredForMouse else canvas.highlightedElement
        elif inputs.inputEvent("UIRIGHT", False):
            if "right" in self.links[canvas.highlightedElement]:
                self.successfulMove(canvas)
                return self.links[canvas.highlightedElement]["right"] if not caredForMouse else canvas.highlightedElement
            
        
        return canvas.highlightedElement