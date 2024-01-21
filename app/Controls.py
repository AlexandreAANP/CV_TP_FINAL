from Events.EventsTrigger import EventsTrigger
from Events.SelectEvent import SelectEvent
from Events.OpenAppEvent import OpenAppEvent
from Events.CloseAppEvent import CloseAppEvent
from MiniApps.DrawApp.Draw import Draw
from MiniApps.FaceReplaceApp.FaceReplace import FaceReplace
from MiniApps.MiniApp import MiniApp
from Icon import Icon
import cv2 as cv
import time
class Controls:
    instance = None
    def __init__(self):
        self.instance = self
        self.eventstrigger = EventsTrigger.get()
        self.icons = MiniApp.getAllAppIcons()
        self.Object = None
        self.start = None
        
    @classmethod
    def get(cls):
        if Controls.instance is None:
            Controls.instance = Controls()
        return Controls.instance
        
    def setObjectTime(self, coords, Object):
        if self.Object != Object:
            self.start = time.time()
            self.Object = Object
            return
        if time.time() - self.start > 2:
            if Draw.get().isOpen:
                if self.Object == Draw.get().clear_icon:
                    self.start = None
                    self.Object = None
                    Draw.get().clean()
                if self.Object == Draw.get().save_icon:
                    self.start = None
                    self.Object = None
                    Draw.get().save()
            if FaceReplace.get().isOpen:
                if self.Object == FaceReplace.get().left_icon:
                    self.start = None
                    self.Object = None
                    FaceReplace.get().change_face("left")
                elif self.Object == FaceReplace.get().rigth_icon:
                    self.start = None
                    self.Object = None
                    FaceReplace.get().change_face("right")

           
            if type(self.Object) is Icon:
                to_open = MiniApp.get_app_by_icon(self.Object)
                if to_open:
                    self.start = None
                    self.Object = None
                    OpenAppEvent(coords, to_open)
            if type(self.Object) is Draw:
                self.start = None
                self.Object = None
                return CloseAppEvent(coords, Draw.get_app_name())
            
        
    def checkEvents(self,frame):
        while self.eventstrigger.length > 0:
            event = self.eventstrigger.pop()
            if event is None:
                return
            elif event.type is OpenAppEvent:
                MiniApp.OpenApp(event.app_name)
            elif event.type is CloseAppEvent:
                MiniApp.CloseAllApps()
            elif event.type is SelectEvent:
                #Mouse select
                #frame = cv.circle(frame, (int(event.coords[0]*frame.shape[1]), int(event.coords[1]*frame.shape[0])), 5, (255, 0, 255), -1)
                oppened_app = MiniApp.which_app_is_open()
                if oppened_app:
                    print(oppened_app)
                    if oppened_app == FaceReplace.get_app_name():
                        if FaceReplace.get().in_range_left_icon(event.coords, frame):
                            self.setObjectTime(event.coords, FaceReplace.get().left_icon)
                        if FaceReplace.get().in_range_right_icon(event.coords, frame):
                            self.setObjectTime(event.coords, FaceReplace.get().rigth_icon)
                        if FaceReplace.get().icon.inRange(event.coords, frame):
                            self.setObjectTime(event.coords, FaceReplace.get().icon)
                    elif oppened_app == Draw.get_app_name():
                        if Draw.get().in_range_close(event.coords, frame):
                            self.setObjectTime(event.coords, Draw.get())
                        if Draw.get().in_range_clear(event.coords, frame):
                            self.setObjectTime(event.coords, Draw.get().clear_icon)
                        if Draw.get().in_range_save(event.coords, frame):
                            self.setObjectTime(event.coords, Draw.get().save_icon)
                else:    
                    for icon in self.icons:
                        if icon.inRange(event.coords, frame):
                            self.setObjectTime(event.coords,icon)
                    
    
    