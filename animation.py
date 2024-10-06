class Animation:
    def __init__(self, frames=[], fps=1, loops = True):
        self.frames = frames
        self.fps = fps
        self.currentFrame = 0
        self.framesTilNextFrame = 60/fps
        
        self.loops = loops
        self.finished = False
    
    def getFrame(self):
        self.framesTilNextFrame-=1 if not self.finished else 0
        if self.framesTilNextFrame == 0:
            self.framesTilNextFrame = 60/self.fps
            self.currentFrame+=1
            if self.currentFrame == len(self.frames): 
                self.currentFrame = 0
                if not self.loops:
                    self.finished = True
        
        return self.frames[self.currentFrame]
    
    def reset(self):
        self.currentFrame = 0
        self.framesTilNextFrame = 60/self.fps
        
        self.finished = False
