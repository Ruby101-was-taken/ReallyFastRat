from scripts.tiles.tiles import *

def createTile(x, y, tileID, image=pygame.Surface((0, 0))):
    match tileID:
        case 0:
            return GroundTile(x,y,tileID)
        case 1:
            return SemiSolidTile(x,y,tileID)
        case 2:
            return SpikeTile(x,y,tileID)
        case 4:
            return SpringTile(x,y,tileID, 20)
        case 5:
            return BoosterTile(x,y,tileID, 13)
        case 6:
            return SpringTile(x,y,tileID, 13)
        case 7:
            return BoosterTile(x,y,tileID, -13)
        case 8:
            return SpringTile(x,y,tileID, -20)
        case 9:
            return Balloon(x,y,tileID, tileImages.objectImages[8])
        case 10:
            return Slime(x,y,tileID, image)
        case 12:
            return Coin(x,y,tileID, tileImages.objectImages[9])
        case 13:
            return SuperCoin(x,y,tileID, tileImages.objectImages[10])
        case 14:
            return Checkpoint(x,y,tileID)
        case 15:
            return GroundTile(x,y,tileID)
        case 16:
            return GroundTile(x,y,tileID)
        case 17:
            return GroundTile(x,y,tileID)
        case 18:
            return BgTile(x,y,tileID)
        case 19:
            return BgTile(x,y,tileID)
        case 20:
            return BgTile(x,y,tileID)
        case 21:
            return BgTile(x,y,tileID)
        case 22:
            return MovingPlatform(x,y,tileID, (0,0))
        case 23:
            return EndGoal(x,y,tileID)
        case 24:
            return DeathPlane(x,y,tileID)
        case 25:
            return InstantSpawner(x,y,tileID, None, 1, 1)
        case 26:
            return DashRefill(x,y,tileID)
        case 27:
            return ToggleBlock(x,y,tileID, state=True, toggledImage=tileImages.objectImages[16])
        case 28:
            return ToggleBlock(x,y,tileID, state=False, toggledImage=tileImages.objectImages[17])
        case 29:
            return ToggleSwitch(x,y,tileID, state=True)
        case 30:
            return ToggleSwitch(x,y,tileID, state=False)
        case 31:
            return StopLessThanX(x,y,tileID, 0)
        case 32:
            return StopLessThanY(x,y,tileID, 0)
        case 33:
            return StopMoreThanX(x,y,tileID, 0)
        case 34:
            return StopMoreThanY(x,y,tileID, 0)
        case 35:
            return Alarm(x,y,tileID, 20, 20, {}, resources.entityImages["evilRat"][0])
        case 36:
            return Ramp(x, y, tileID, resources.slope)
        case 37:
            return LevelChange(x, y, tileID)
        case 38:
            return CannotMove(x, y, tileID)
        case _:
            return StaticTile(x,y,tileID)