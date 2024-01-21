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
    def check_events(self,frame):
        while self.eventstrigger.length > 0:
            event = self.eventstrigger.pop()
            if event is None:
                return
            elif event.type is OpenAppEvent:
                MiniApp.open_app(event.app_name)
                MiniApp.close_all_app_icons()
            elif event.type is CloseAppEvent:
                MiniApp.close_all_apps()
            elif event.type is SelectEvent:
                oppened_app = MiniApp.which_app_is_open()
                if oppened_app:
                    if oppened_app == FaceReplace.get_app_name():
                        FaceReplace.get().event(event, frame)
                    elif oppened_app == Draw.get_app_name():
                        Draw.get().event(event, frame)
                else:    
                    for icon in MiniApp.get_all_app_icons():
                        icon.event(event, frame)
                    
    @classmethod
    def get(cls):
        if Controls.instance is None:
            Controls.instance = Controls()
        return Controls.instance
    