import pygame
class AudioSource:
    def __init__(self, soundPath:str) -> None:
        self.sound = pygame.mixer.Sound("sound/" + soundPath)