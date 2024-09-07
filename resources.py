import pygame

from audioSource import AudioSource


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

sounds = {
    "click": AudioSource("ui/click.wav"),
    "menuChange": AudioSource("ui/menuChange.wav"),
    "rat": AudioSource("rat/rat.mp3")
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
    ],
    
    "controlLayouts": {
        "xbox": pygame.image.load("ui/controls/controller/xbox.png").convert_alpha()
    }, 
    
    "rankings": {
        "e": pygame.image.load("ui/results/e.png").convert_alpha(),
        "d": pygame.transform.scale(pygame.image.load("ui/results/d.png"), (321, 321)).convert_alpha(),
        "c": pygame.transform.scale(pygame.image.load("ui/results/c.png"), (321, 321)).convert_alpha(),
        "b": pygame.transform.scale(pygame.image.load("ui/results/b.png"), (321, 321)).convert_alpha(),
        "a": pygame.transform.scale(pygame.image.load("ui/results/a.png"), (321, 321)).convert_alpha(),
        "s": pygame.transform.scale(pygame.image.load("ui/results/s.png"), (321, 321)).convert_alpha()
    },
    
    "levelName": {
        "bg": pygame.image.load("ui/levelName/bg.png").convert_alpha()
    },
    
    "HUD": {
        "fullBoost": pygame.image.load("ui/HUD/fullBoost.png")
    }
}

hats = {
    "top": pygame.image.load("player/hats/top.png").convert_alpha(),
    "fire": pygame.image.load("player/hats/fire.png").convert_alpha(),
    "flower": pygame.image.load("player/hats/flower.png").convert_alpha(),
    "propeller": pygame.image.load("player/hats/propeller.png").convert_alpha(),
    "hard": pygame.image.load("player/hats/hard.png").convert_alpha(),
}

def sliceTilemap(sheet, w, h):
    spliedImages = []  # This list will hold your individual tiles
    sheet = sheet.convert_alpha()
    for y in range(0, sheet.get_height(), h):
        for x in range(0, sheet.get_width(), w):
            tile = sheet.subsurface(pygame.Rect(x, y, w, h)).convert_alpha()
            spliedImages.append(tile.convert_alpha()) 
    
    return spliedImages
