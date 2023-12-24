import cv2 as cv
import numpy as np
import Colors

from Events.SelectEvent import SelectEvent
from Icon import Icon
class Draw:
    buttonCloseWidth = 35
    buttonCloseHeight = 20
    
    
    this = None
    def __init__(self, drawIconPath: str, saveIconPath: str, width = 640, height = 480):
        self.clearIcon = Icon(drawIconPath, (0, int(height*0.25)),"cleanIcon", 0.5, False)
        self.saveIcon = Icon(saveIconPath, (0, int(height*0.25)+10+self.clearIcon.height),"saveIcon", 0.5, False)
        self.landmarks = None
        self.width = width
        self.heigth = height 
        self.isOpen = False
        self.baseFrame = self.DrawBaseBackground()
        self.lastDraw = self.baseFrame.copy()
        Draw.this = self
       
    def DrawBaseBackground(self):
        baseFrame = np.zeros((self.heigth, self.width, 3), np.uint8)
        baseFrame = self.drawNavBar(baseFrame)
        baseFrame = self.drawWhiteBoard(baseFrame)
        return baseFrame
        
    def run(self, landmarks):
        if not self.isOpen:
            return None
        self.lastDraw = self.clearIcon.putImageInFrame(self.lastDraw)
        self.lastDraw = self.saveIcon.putImageInFrame(self.lastDraw)
        self.landmarks = landmarks
        shouldDraw = self.DrawGesture(landmarks)
        if shouldDraw:
            self.lastDraw = self.drawPoint(shouldDraw, self.lastDraw, shouldDraw[2])
        self.lastDraw = self.drawNavBar(self.lastDraw)
        return self.lastDraw.copy()
        
    def DrawGesture(self, landmarks):
        if landmarks is None or landmarks.right_hand_landmarks is None:
            return False
        FingersUp = SelectEvent.detectWhichFingerIsUp(landmarks.right_hand_landmarks.landmark)
        if len(FingersUp) <= 3 and "INDEX" in FingersUp.keys() and "MIDDLE" in FingersUp.keys():
            x = (FingersUp["INDEX"][0].x + FingersUp["MIDDLE"][0].x)/2
            y = (FingersUp["INDEX"][0].y + FingersUp["MIDDLE"][0].y)/2
            return (x,y, Colors.RED)
        if len(FingersUp) > 4:
            x =0
            y = 0
            i=0
            for finger in FingersUp.keys():
                if finger != "THUMB":
                    x += FingersUp[finger][0].x
                    y += FingersUp[finger][0].y
                    i+=1
            x = x/i
            y = y/i
            return (x,y, Colors.WHITE)
        return False
    
    def drawPoint(self, coords, frame, color):
        if color == Colors.WHITE:
            frame = cv.circle(frame, (int(coords[0]*frame.shape[1]), int(coords[1]*frame.shape[0])), 20, color, -1)
        else:
            frame = cv.circle(frame, (int(coords[0]*frame.shape[1]), int(coords[1]*frame.shape[0])), 5, color, -1)
        return frame
        
    def drawNavBar(self, frame):
        frame = cv.rectangle(frame, (0,0), (frame.shape[1], 20), Colors.GRAY, -1)
        #X BUTTON
        frame = cv.rectangle(frame, (0,0), (Draw.buttonCloseWidth, Draw.buttonCloseHeight), Colors.RED, -1)
        frame = cv.putText(frame, "X", (15, 15), cv.FONT_HERSHEY_PLAIN, 0.7, (255, 255, 255), 1)
        return frame
        
    def drawWhiteBoard(self, frame):
        frame = cv.rectangle(frame, (0,20), (frame.shape[1], frame.shape[0]), (255,255,255), -1)
        return frame
        
    def inRangeClose(self, coords, frame):
        if not self.isOpen:
            return False
        return coords[0]*frame.shape[1] >= 0 and coords[0]*frame.shape[1] <= Draw.buttonCloseWidth and coords[1]*frame.shape[0] >= 0 and coords[1]*frame.shape[0] <= Draw.buttonCloseHeight
    
    def inRangeClear(self, coords, frame):
        if not self.isOpen:
            return False
        return coords[0]*frame.shape[1] >= self.clearIcon.x and coords[0]*frame.shape[1] <= self.clearIcon.x + self.clearIcon.width and coords[1]*frame.shape[0] >= self.clearIcon.y and coords[1]*frame.shape[0] <= self.clearIcon.y + self.clearIcon.height
    
    def clean(self):
        self.lastDraw = self.baseFrame.copy()
        
    def inRangeSave(self, coords, frame):
        if not self.isOpen:
            return False
        return coords[0]*frame.shape[1] >= self.saveIcon.x and coords[0]*frame.shape[1] <= self.saveIcon.x + self.saveIcon.width and coords[1]*frame.shape[0] >= self.saveIcon.y and coords[1]*frame.shape[0] <= self.saveIcon.y + self.saveIcon.height    
        
    def save(self):
        saveImage = self.lastDraw.copy()
        import os
        import datetime
        dir_path = os.path.dirname(os.path.realpath(__file__))
        saveImage = self.removeNavBar(saveImage)
        saveImage = self.removeIcons(self.clearIcon, saveImage)
        saveImage = self.removeIcons(self.saveIcon, saveImage)
        saveImage = cv.flip(saveImage, 1)
        cv.imwrite(f'{dir_path}/SavedDrawImages/image_saved_{str(datetime.datetime.now().strftime("%Y_%m_%d__%I_%M_%S_%p"))}.png', saveImage)
        
    def removeNavBar(self, frame):
        frame = cv.rectangle(frame, (0,0), (frame.shape[1], 20), Colors.WHITE, -1)
        return frame
        
    def removeIcons(self, icon, frame):
        frame = cv.rectangle(frame, (icon.x,icon.y), (icon.x+icon.width, icon.y+icon.height), Colors.WHITE, -1)
        return frame
        
    def open(self):
        self.clearIcon.show()
        self.clearIcon.show()
        self.isOpen = True       
    
    def close(self):
        self.clearIcon.hide()
        self.saveIcon.hide()
        self.isOpen = False
        
    
    