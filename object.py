import pygame


class Object:
    def __init__(self, x, y, name, objType, level, customProperties, gid=0):
        self.x = x
        self.y = y
        self.name = name
        self.type = objType
        self.customProperties = customProperties
        
        
        if self.type == "tile": # only spawning a tile if we are a tile type object
            from scripts.tiles.createTile import createTile
            gid-=1 # gid stores the tile value at a value one greater than the tile index, so we just bring it down
            #                               minus 20 cuz the y is off by 20
            newTile = createTile(self.x, self.y-20, gid)
            newTile.object = self
            level.addTile(newTile)
            
            
    def getProperty(self, propertyName):
        for prop in self.customProperties["properties"]:
            if prop["name"] == propertyName:
                return prop["value"]
        return None
    def hasProperty(self, propertyName):
        for prop in self.customProperties["properties"]:
            if prop["name"] == propertyName:
                return True
        return False