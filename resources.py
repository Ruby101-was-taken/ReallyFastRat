import pygame

from audioSource import AudioSource


#LOAD IMAGES 
def reloadPlayerImages(hatType = "none"):
    playerImages = [
        pygame.image.load("player/player.png").convert_alpha(),#0
        pygame.image.load("player/walk1.png").convert_alpha(),#1
        pygame.image.load("player/walk2.png").convert_alpha(),#2
        pygame.image.load("player/fall0.png").convert_alpha(),#3
        pygame.image.load("player/fall1.png").convert_alpha(),#4
        pygame.image.load("player/fall2.png").convert_alpha(),#5
        pygame.image.load("player/jump1.png").convert_alpha(),#6
        pygame.image.load("player/jump2.png").convert_alpha(),#7
        pygame.image.load("player/run0.png").convert_alpha(),#8
        pygame.image.load("player/run1.png").convert_alpha(),#9
        pygame.image.load("player/run2.png").convert_alpha(),#10
        pygame.image.load("player/climbHold.png").convert_alpha(),#11
        pygame.image.load("player/climbUp1.png").convert_alpha(),#12
        pygame.image.load("player/climbUp2.png").convert_alpha(),#13
        pygame.image.load("player/bounceFront.png").convert_alpha(),#14
        pygame.image.load("player/bounceRight.png").convert_alpha(),#15
        pygame.image.load("player/bounceBack.png").convert_alpha(),#16
        pygame.image.load("player/bounceLeft.png").convert_alpha(),#17
        pygame.image.load("player/blink1.png").convert_alpha(),#18
        pygame.image.load("player/blink2.png").convert_alpha(),#19
        pygame.image.load("player/turn1.png").convert_alpha(),#20
        pygame.image.load("player/turn2.png").convert_alpha(),#21
        pygame.image.load("player/sit1.png").convert_alpha(),#22
        pygame.image.load("player/sit2.png").convert_alpha(),#23
        pygame.image.load("player/sit3.png").convert_alpha(),#24
        pygame.image.load("player/sit4.png").convert_alpha(),#25
        pygame.image.load("player/sit5.png").convert_alpha(),#26
        
        
        #always have this be the last item
        [
            pygame.image.load(f"player/hats/{hatType}/player.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/walk1.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/walk2.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/fall0.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/fall1.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/fall2.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/jump1.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/jump2.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/run0.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/run1.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/run2.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/climbHold.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/climbUp1.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/climbUp2.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/bounceFront.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/bounceRight.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/bounceBack.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/bounceLeft.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/player.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/player.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/turn1.png").convert_alpha(),
            pygame.image.load(f"player/hats/{hatType}/turn2.png").convert_alpha()
        ] if hatType != "none" else []
    ]
    print(len(playerImages[-1]))
    return playerImages


playerImages = reloadPlayerImages()
playerHatImages = playerImages[-1]

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
    "rat": AudioSource("rat/rat.mp3"),
    "menuMove": AudioSource("ui/menuMove.wav"),
    
    "player": {"dash": AudioSource("game/player/dash.wav"),
               "jump": AudioSource("game/player/jump.wav")}
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


def sliceTilemap(sheet, w, h):
    spliedImages = []  # This list will hold your individual tiles
    sheet = sheet.convert_alpha()
    for y in range(0, sheet.get_height(), h):
        for x in range(0, sheet.get_width(), w):
            tile = sheet.subsurface(pygame.Rect(x, y, w, h)).convert_alpha()
            spliedImages.append(tile.convert_alpha()) 
    
    return spliedImages
