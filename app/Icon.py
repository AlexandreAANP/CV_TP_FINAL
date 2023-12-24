import cv2 as cv
from Utils import replaceBackgroundOfImage, CreateMask
import time
class Icon:
    WIDTH = 70
    HEIGHT = 70
    CLICK_TIME_SECONDS = 2
    def __init__(self,path :str, coords: tuple,name, f:float = 1.0, isHidden = True):
        self.name = name
        self.x = coords[0]
        self.y = coords[1]
        self.width = int(Icon.WIDTH * f)
        self.height = int(Icon.HEIGHT * f)
        self.image = cv.imread(path)
        self.image = cv.resize(self.image, (self.width, self.height))
        self.mask = CreateMask(cv.imread(path, cv.IMREAD_UNCHANGED))
        self.mask = cv.resize(self.mask, (self.width, self.height))
        self.IsInRange = False
        self.beginClickTime = None
        self.isHidden = False

    def hide(self):
        self.isHidden = True
    
    def show(self):
        self.isHidden = False
    def putImageInFrame(self, screen):
        if self.isHidden:
            return screen
        partOfScreen = screen[self.y:self.y+self.height, self.x:self.x+self.width]
        self.image = replaceBackgroundOfImage(self.image, partOfScreen, self.mask)
        screen[self.y:self.y+self.height, self.x:self.x+self.width] = self.image
        return screen
    
    def inRange(self, coords, frame):
        if self.isHidden:
            return False
        return (coords[0]*frame.shape[1] >= self.x
                and coords[0]*frame.shape[1] <= self.x + self.width
                and coords[1]*frame.shape[0] >= self.y
                and coords[1]*frame.shape[0] <= self.y + self.height)
    
    def startClickTime(self):
        if self.beginClickTime is None:
            self.beginClickTime = time.time()
    
    def resetClickTime(self):
        self.beginClickTime = None
        
        