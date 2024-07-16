import pygame



#LOAD IMAGES 
def reloadPlayerImages():
    playerImages = [
        pygame.image.load("player/player.png").convert_alpha(),
        pygame.image.load("player/walk1.png").convert_alpha(),
        pygame.image.load("player/walk2.png").convert_alpha(),
        pygame.image.load("player/fall0.png").convert_alpha(),
        pygame.image.load("player/fall1.png").convert_alpha(),
        pygame.image.load("player/fall2.png").convert_alpha(),
        pygame.image.load("player/jump1.png").convert_alpha(),
        pygame.image.load("player/jump2.png").convert_alpha(),
        pygame.image.load("player/run0.png").convert_alpha(),
        pygame.image.load("player/run1.png").convert_alpha(),
        pygame.image.load("player/run2.png").convert_alpha(),
        pygame.image.load("player/climbHold.png").convert_alpha(),
        pygame.image.load("player/climbUp1.png").convert_alpha(),
        pygame.image.load("player/climbUp2.png").convert_alpha(),
        pygame.image.load("player/bounceFront.png").convert_alpha(),
        pygame.image.load("player/bounceRight.png").convert_alpha(),
        pygame.image.load("player/bounceBack.png").convert_alpha(),
        pygame.image.load("player/bounceLeft.png").convert_alpha(),
    ]
    return playerImages


playerImages = reloadPlayerImages()

slope = pygame.image.load("objects/slope.png").convert_alpha()

tile_width = 20
tile_height = 20  # Replace with your tile height

entityImages ={
    "evilRat" : [
        pygame.image.load("entities/enemy/evilRat/evilRat.png").convert_alpha()
    ]
}


uiAnimations = {
    "bluePrints": [
        pygame.image.load("ui/playerBluePrints/playerBluePrints00.png").convert_alpha(),
        pygame.image.load("ui/playerBluePrints/playerBluePrints01.png").convert_alpha(),
        pygame.image.load("ui/playerBluePrints/playerBluePrints02.png").convert_alpha(),
        pygame.image.load("ui/playerBluePrints/playerBluePrints03.png").convert_alpha(),
        pygame.image.load("ui/playerBluePrints/playerBluePrints04.png").convert_alpha(),
        pygame.image.load("ui/playerBluePrints/playerBluePrints05.png").convert_alpha(),
        pygame.image.load("ui/playerBluePrints/playerBluePrints06.png").convert_alpha(),
        pygame.image.load("ui/playerBluePrints/playerBluePrints07.png").convert_alpha(),
        pygame.image.load("ui/playerBluePrints/playerBluePrints08.png").convert_alpha(),
        pygame.image.load("ui/playerBluePrints/playerBluePrints09.png").convert_alpha(),
        pygame.image.load("ui/playerBluePrints/playerBluePrints10.png").convert_alpha()
        ],
    
    "bgDetail": [
        pygame.image.load("ui/settings/noDetail.png").convert_alpha(),
        pygame.image.load("ui/settings/minDetail.png").convert_alpha(),
        pygame.image.load("ui/settings/fullDetail.png").convert_alpha()
    ]
}


def sliceTilemap(sheet, w, h):
    spliedImages = []  # This list will hold your individual tiles
    sheet = sheet.convert_alpha()
    for y in range(0, sheet.get_height(), h):
        for x in range(0, sheet.get_width(), w):
            tile = sheet.subsurface(pygame.Rect(x, y, w, h)).convert_alpha()
            spliedImages.append(tile.convert_alpha()) 
    
    return spliedImages
