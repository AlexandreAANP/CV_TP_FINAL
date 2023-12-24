from Events.EventsTrigger import EventsTrigger
from Events.SelectEvent import SelectEvent
from Events.OpenFaceReplaceAppEvent import OpenFaceReplaceAppEvent
from Events.OpenDrawAppEvent import OpenDrawAppEvent
from Events.CloseDrawAppEvent import CloseDrawAppEvent
from MiniApps.DrawApp.Draw import Draw
from MiniApps.FaceReplaceApp.FaceReplace import FaceReplace
from Icon import Icon
import cv2 as cv
import time
class Controls:
    def __init__(self, icons : list):
        self.eventstrigger = EventsTrigger.this
        self.icons = icons
        self.Object = None
        self.start = None
        
    def setObjectTime(self, coords, Object):
        if self.Object != Object:
            self.start = None
        self.Object = Object
        if self.start is None:
            self.start = time.time()
        if time.time() - self.start > 2:
            if Draw.this.isOpen:
                if self.Object == Draw.this.clearIcon:
                    self.start = None
                    self.Object = None
                    Draw.this.clean()
                if self.Object == Draw.this.saveIcon:
                    self.start = None
                    self.Object = None
                    Draw.this.save()
            if type(self.Object) is Icon:
                if not FaceReplace.this.isOpen and self.Object.name == "DrawApp":
                    self.start = None
                    self.Object = None
                    return OpenDrawAppEvent(coords)
                if not Draw.this.isOpen and self.Object.name == "FaceReplaceApp":
                    self.start = None
                    self.Object = None
                    return OpenFaceReplaceAppEvent(coords)
            if type(self.Object) is Draw:
                self.start = None
                self.Object = None
                return CloseDrawAppEvent(coords)
            
    
    def resetTime():
        pass
        
    def checkEvents(self, frame):
        while self.eventstrigger.length > 0:
            event = self.eventstrigger.pop()
            if event is None:
                continue
            if event.type is CloseDrawAppEvent:
                Draw.this.close()
                for icon in self.icons:
                    icon.show()
            if event.type is OpenDrawAppEvent:
                Draw.this.open()
                for icon in self.icons:
                    icon.hide()
                cv.putText(frame, "CLICK ICON", (200, 200), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            if event.type is OpenFaceReplaceAppEvent:
                FaceReplace.this.open()
            if event.type is SelectEvent:
                if Draw.this.isOpen:
                    if Draw.this.inRangeClose(event.coords, frame):
                        self.setObjectTime(event.coords, Draw.this)
                    if Draw.this.inRangeClear(event.coords, frame):
                        self.setObjectTime(event.coords, Draw.this.clearIcon)
                    if Draw.this.inRangeSave(event.coords, frame):
                        self.setObjectTime(event.coords, Draw.this.saveIcon)
                else:    
                    for icon in self.icons:
                        if icon.inRange(event.coords, frame):
                            self.setObjectTime(event.coords,icon)
                    cv.putText(frame, "Select", (200, 200), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
    
    