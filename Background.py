import pygame


class Background:
    def __init__(self, image, parallax):
        self.parallax = parallax
        
        self.w = image.get_width()
        
        self.surface = pygame.Surface((self.w*2, 720), pygame.SRCALPHA)
        self.surface.blit(image, (0,0))
        self.surface.blit(image, (self.w,0))
        
    def draw(self, win, camx):
        pos = ((-camx / self.parallax) % self.w) - self.w
        drawSurf = self.surface.subsurface((abs(pos), 0), (1280, 720))
        win.blit(drawSurf, (0, 0))