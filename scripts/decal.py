

class Decal:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
    def draw(self, surf, offset):
        surf.blit(self.img, (self.x, self.y+offset))