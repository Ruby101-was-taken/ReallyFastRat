

import random
import pygame, os, sys
from pygame.locals import *
from ratFacts import facts


smallFont = pygame.font.SysFont("arial", 20)

pygame.joystick.init()


def quitGame():
    pygame.quit()
    sys.exit()

def getController(numOfJoy, joy):
    class Button():
        def __init__(self, x, y, width, height, buttonText='Button', ID = 0):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.ID = ID
            self.alreadyPressed = False

            self.fillColors = {
                'normal': '#ffffff',
                'hover': '#666666',
                'pressed': '#333333',
            }
            
            self.buttonSurface = pygame.Surface((self.width, self.height))
            self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

            self.buttonSurf = smallFont.render(buttonText, True, (20, 20, 20))

            self.buttonText = buttonText
        
        def process(self):
            mousePos = pygame.mouse.get_pos()
            if self.buttonRect.collidepoint(mousePos):
                
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    return self.ID
                else:
                    return -1
            else:
                return -1
        def draw(self):
            mousePos = pygame.mouse.get_pos()
            self.buttonSurface.fill(self.fillColors['normal'])
            if self.buttonRect.collidepoint(mousePos):
                self.buttonSurface.fill(self.fillColors['hover'])
                self.buttonSurface.blit(images[1], (self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2 - 35, 5))
                self.buttonSurface.blit(images[1], (self.buttonRect.width/2 + self.buttonSurf.get_rect().width/2 + 5, 5))
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.buttonSurface.fill(self.fillColors['pressed'])
            self.buttonSurface.blit(self.buttonSurf, [
                self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
                self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
            ])
            win.blit(self.buttonSurface, self.buttonRect)
    pygame.init()

    controllerSelected = False
    smallFont = pygame.font.SysFont("arial", 20)
    bigFont = pygame.font.SysFont("arial", 50)

    buttons = []
    for button in range(numOfJoy):
        buttons.append(Button(0, 25+(40*button), 1280, 40, joy.Joystick(button).get_name(), button))
        joy.Joystick(button).init()
    factHeight = 50+(40*len(buttons))
        
    images = [pygame.image.load('logo/logoDecorSmol.png'), pygame.image.load('player/player.png')]
    bgImages = [pygame.image.load("backgrounds/city/bg.png"), pygame.image.load("backgrounds/city/layer1.png"), pygame.image.load("backgrounds/city/layer2.png")]
    fact = random.choice(facts)
    factSurf = smallFont.render(fact, True, (255, 255, 255))
    factBG = pygame.Surface((1280, factSurf.get_height()))
    factBG.fill((0,0,0))
    
    factButton = Button(0, factHeight + factBG.get_height() + 10, 300, 40, "New Fact", 100)
    factButtonClick = True
    
    currentTestJoy = 0

    win = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Multiple Controllers Conected!")
    while not controllerSelected:  
        currentTestJoy += 0.1
        if currentTestJoy >= numOfJoy:
            currentTestJoy = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                controllerSelected = True
                quitGame()
        if not controllerSelected:
            for image in bgImages:
                win.blit(image, (0,0))
            win.blit(images[0], (1140, 670))
            win.blit(factBG, (0,0))
            win.blit(smallFont.render(f"There are {numOfJoy} controllers connected. Select one with your mouse to continue, or hold both shoulder buttons on the controller you want to connect(You can still use keyboard in game!)", True, (255, 255, 255)), (0,0))
            
            win.blit(factBG, (0, factHeight))
            win.blit(factSurf, (0, factHeight))
            
            if factButtonClick:
                factButtonClick = pygame.mouse.get_pressed(num_buttons=3)[0]

            for button in buttons:
                button.draw()
                if button.process() != -1 and not factButtonClick:
                    controllerSelected = True
                    return button.ID
                factButton.draw()
                if factButton.process() != -1 and not factButtonClick:
                    fact = random.choice(facts)
                    factSurf = smallFont.render(fact, True, (255, 255, 255))
                    factBG = pygame.Surface((1280, factSurf.get_height()))
                    factBG.fill((0,0,0))
        
                    factButton = Button(0, factHeight + factBG.get_height() + 10, 300, 40, "New Fact", 100)
                    
                    factButtonClick = True

            tempJoy = pygame.joystick.Joystick(int(currentTestJoy))
            tempJoy.init()
            buttonsList = [tempJoy.get_button(i) for i in range(tempJoy.get_numbuttons())]
            if (1 == buttonsList[9] and 1 == buttonsList[10]) or (1 == buttonsList[4] and 1 == buttonsList[5]):
                win.blit(factBG, (0,0))
                win.blit(smallFont.render(f"{tempJoy.get_name()} was found", True, (255, 255, 255)), (0,0))
                pygame.display.flip()
                return int(currentTestJoy)
                
                    

            pygame.display.flip()
    
    return -1