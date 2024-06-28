class Animation:
    def __init__(self, frames=[], fps=1):
        self.frames = frames
        self.fps = fps
        self.currentFrame = 0
        self.framesTilNextFrame = 60/fps
    
    def getFrame(self):
        self.framesTilNextFrame-=1
        if self.framesTilNextFrame == 0:
            self.framesTilNextFrame = 60/self.fps
            self.currentFrame+=1
            if self.currentFrame == len(self.frames): self.currentFrame = 0
        
        return self.frames[self.currentFrame]