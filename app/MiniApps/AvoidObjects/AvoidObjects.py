import Utils
import cv2 as cv
import time
from MiniApps.MiniApp import MiniApp
from Icon import Icon
class AvoidObjects(MiniApp):
    __app_name = "AvoidObjects"
    instance = None
    def __init__(self, path_animations: str, path_animations_mask: str, width : int, height: int):
        super().__init__(AvoidObjects.__app_name, 
                         Icon(Utils.PROJECT_PATH+"/images/AvoidObjectsLogo.png",(0,45+Icon.HEIGHT+10),
                        AvoidObjects.__app_name))
        AvoidObjects.instance = self
        
        self.animation = []
        self.animations = Utils.getAllFilesPathFromFolder(path_animations)
        self.animationsMask = Utils.getAllFilesPathFromFolder(path_animations_mask)

        for image in self.animations:
            self.animation.append((cv.resize(cv.imread(image), (width, height)),
                                  cv.resize(cv.imread(image, cv.THRESH_BINARY), (width,height))))
        self.indexFrame = 0
        
    @classmethod
    def get(cls):
        if cls.instance:
            return cls.instance
        raise Exception("AvoidObjects not initialized")   
    
    @classmethod
    def get_app_name(cls):
        return cls.__app_name 
        
    def getAnimationAndMaskPath(self):
        self.indexFrame += 1
        if self.indexFrame >= len(self.animations):
            self.indexFrame = 0
        yield (self.animations[self.indexFrame], self.animationsMask[self.indexFrame])
    def run(self, landmarks, frame):
        if not self.isOpen:
            return frame
        start = time.time()
        
        if self.indexFrame >= len(self.animation):
            self.indexFrame = 0
        #get animations
        frameAnimation, frameAnimationMask = self.animation[self.indexFrame]
        self.indexFrame +=1
        
        start = time.time()
        frame = Utils.replaceBackgroundOfImage(frameAnimation, frame, frameAnimationMask)
        end = time.time()
        print("replaceBackground", end-start)
        return frame
    
    def open(self):
        self.isOpen = True
        
    def close(self):
        self.isOpen = False
        