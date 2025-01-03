import pygame

from audioSource import AudioSource

class ResourceManager:
    
    #LOAD IMAGES 
    def reloadPlayerImages(self, hatType = "none"):
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
        return playerImages

    def __init__(self):
        
        self.playerImages = self.reloadPlayerImages()
        self.playerHatImages = self.playerImages[-1]

        self.slope = pygame.image.load("objects/slope.png").convert_alpha()

        self.tile_width = 20
        self.tile_height = 20  # Replace with your tile height

        self.entityImages ={
            "evilRat" : [
                pygame.image.load("entities/enemy/evilRat/evilRat.png").convert_alpha()
            ]
        }

        self.sounds = {
            "click": AudioSource("ui/click.wav"),
            "menuChange": AudioSource("ui/menuChange.wav"),
            "rat": AudioSource("rat/rat.mp3"),
            "menuMove": AudioSource("ui/menuMove.wav"),
            
            "player": {"dash": AudioSource("game/player/dash.wav"),
                    "jump": AudioSource("game/player/jump.wav")}
        }

        self.uiAnimations = {
            "bluePrints": [
                pygame.image.load("ui/rat/playerBluePrints/playerBluePrints00.png").convert_alpha(),
                pygame.image.load("ui/rat/playerBluePrints/playerBluePrints01.png").convert_alpha(),
                pygame.image.load("ui/rat/playerBluePrints/playerBluePrints02.png").convert_alpha(),
                pygame.image.load("ui/rat/playerBluePrints/playerBluePrints03.png").convert_alpha(),
                pygame.image.load("ui/rat/playerBluePrints/playerBluePrints04.png").convert_alpha(),
                pygame.image.load("ui/rat/playerBluePrints/playerBluePrints05.png").convert_alpha(),
                pygame.image.load("ui/rat/playerBluePrints/playerBluePrints06.png").convert_alpha(),
                pygame.image.load("ui/rat/playerBluePrints/playerBluePrints07.png").convert_alpha(),
                pygame.image.load("ui/rat/playerBluePrints/playerBluePrints08.png").convert_alpha(),
                pygame.image.load("ui/rat/playerBluePrints/playerBluePrints09.png").convert_alpha(),
                pygame.image.load("ui/rat/playerBluePrints/playerBluePrints10.png").convert_alpha()
                ],
            
            "sad": [
                pygame.transform.scale(pygame.image.load("ui/rat/sad/sad00.png"), (300, 300)).convert_alpha(),
                pygame.transform.scale(pygame.image.load("ui/rat/sad/sad01.png"), (300, 300)).convert_alpha(),
                pygame.transform.scale(pygame.image.load("ui/rat/sad/sad02.png"), (300, 300)).convert_alpha(),
                pygame.transform.scale(pygame.image.load("ui/rat/sad/sad03.png"), (300, 300)).convert_alpha(),
                pygame.transform.scale(pygame.image.load("ui/rat/sad/sad04.png"), (300, 300)).convert_alpha(),
                pygame.transform.scale(pygame.image.load("ui/rat/sad/sad05.png"), (300, 300)).convert_alpha(),
                pygame.transform.scale(pygame.image.load("ui/rat/sad/sad06.png"), (300, 300)).convert_alpha(),
                pygame.transform.scale(pygame.image.load("ui/rat/sad/sad07.png"), (300, 300)).convert_alpha(),
                pygame.transform.scale(pygame.image.load("ui/rat/sad/sad08.png"), (300, 300)).convert_alpha(),
                pygame.transform.scale(pygame.image.load("ui/rat/sad/sad09.png"), (300, 300)).convert_alpha()
                ],
            
            "bgDetail": [
                pygame.image.load("ui/settings/noDetail.png").convert_alpha(),
                pygame.image.load("ui/settings/minDetail.png").convert_alpha(),
                pygame.image.load("ui/settings/fullDetail.png").convert_alpha()
            ],
            
            "controlLayouts": {
                "xbox": pygame.image.load("ui/controls/controller/xbox.png").convert_alpha(),
                "ps": pygame.image.load("ui/controls/controller/playstation.png").convert_alpha(),
                "pc": pygame.image.load("ui/controls/keyboard/keyboard.png").convert_alpha()
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
                "fullBoost": pygame.image.load("ui/HUD/fullBoost.png").convert_alpha()
            }
        }

        self.uiAssets = {
            "pointer": pygame.image.load("ui/HUD/pointer.png").convert_alpha(),
            "sad": pygame.transform.scale(pygame.image.load("ui/rat/sad.png"), (300, 300)).convert_alpha()
        }

    def sliceTilemap(self, sheet, w, h):
        spliedImages = []  # This list will hold your individual tiles
        sheet = sheet.convert_alpha()
        for y in range(0, sheet.get_height(), h):
            for x in range(0, sheet.get_width(), w):
                tile = sheet.subsurface(pygame.Rect(x, y, w, h)).convert_alpha()
                spliedImages.append(tile.convert_alpha()) 
        
        return spliedImages


resources = ResourceManager()