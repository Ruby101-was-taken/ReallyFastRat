import pygame



#LOAD IMAGES 
playerImages = [
    pygame.image.load("player/player.png"),
    pygame.image.load("player/walk1.png"),
    pygame.image.load("player/walk2.png"),
    pygame.image.load("player/fall0.png"),
    pygame.image.load("player/fall1.png"),
    pygame.image.load("player/fall2.png"),
    pygame.image.load("player/jump1.png"),
    pygame.image.load("player/jump2.png"),
    pygame.image.load("player/run0.png"),
    pygame.image.load("player/run1.png"),
    pygame.image.load("player/run2.png")
]
boostImages = [
    pygame.image.load("player/boost0.png"),
    pygame.image.load("player/boost1.png"),
    pygame.image.load("player/boost2.png")
]


slope = pygame.image.load("objects/slope.png")

tile_width = 20
tile_height = 20  # Replace with your tile height



def sliceTilemap(sheet, w, h):
    spliedImages = []  # This list will hold your individual tiles
    sheet = sheet.convert_alpha()
    for y in range(0, sheet.get_height(), h):
        for x in range(0, sheet.get_width(), w):
            tile = sheet.subsurface(pygame.Rect(x, y, w, h)).convert_alpha()
            spliedImages.append(tile.convert_alpha()) 
    
    return spliedImages
