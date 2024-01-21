import cv2 as cv
import numpy as np
import Colors

from Icon import Icon
from MiniApps.MiniApp import MiniApp
from MiniApps.DrawApp.DrawGesture import DrawGesture
from MiniApps.DrawApp.Paint import Paint
from EventInteraction import EventInteraction
from Events.CloseAppEvent import CloseAppEvent
import Utils
class Draw(MiniApp, EventInteraction):    
    __instance = None
    __app_name = "DrawApp"
    def __init__(self, width = 640, height = 480):
        super().__init__(Draw.__app_name,
                         Icon(Utils.PROJECT_PATH+"/images/DrawAppLogo.png",(width-Icon.WIDTH,9), Draw.__app_name))
        Draw.__instance = self
        self.clear_icon = Icon(Utils.PROJECT_PATH+"/images/Draw/newPage.png", (0, int(height*0.25)),"cleanIcon", 0.5, False)
        self.save_icon = Icon(Utils.PROJECT_PATH+"/images/Draw/save.png", (0, int(height*0.25)+10+self.clear_icon.height),"saveIcon", 0.5, False)
        self.draw_gesture = DrawGesture()
        self.paint = Paint(width, height, [self.clear_icon, self.save_icon])
        self.width = width
        self.heigth = height
        self.isOpen = False
        self.event_type = None
    
    def event(self, event, frame):
        if self.should_trigger_event(event):
            if self.in_range_close(event.coords, frame):
                MiniApp.close_all_apps()
                self.reset_event()
            elif self.in_range_clear(event.coords, frame):
                self.paint.clean_draw()
                self.reset_event()
            elif self.in_range_save(event.coords, frame):
                self.paint.save()
                self.reset_event()  
    def run(self, landmarks, frame):
        if not self.isOpen:
            return frame
        action_point = self.draw_gesture.detect(landmarks)
        if action_point:
            if action_point[0] == 1:
                self.paint.draw_point(action_point[1], Colors.RED)
            if action_point[0] == 2:
                self.paint.clean_point(action_point[1])
        frame = self.paint.get_draw()
        frame = self.clear_icon.putImageInFrame(frame)
        frame = self.save_icon.putImageInFrame(frame)
        return frame
    
    def in_range_close(self, coords, frame):
        if not self.isOpen:
            return False
        return coords[0]*frame.shape[1] >= 0 and coords[0]*frame.shape[1] <= Paint.BUTTON_CLOSE_WIDTH and coords[1]*frame.shape[0] >= 0 and coords[1]*frame.shape[0] <= Paint.BUTTON_CLOSE_HEIGHT
    
    def in_range_clear(self, coords, frame):
        if not self.isOpen:
            return False
        return coords[0]*frame.shape[1] >= self.clear_icon.x and coords[0]*frame.shape[1] <= self.clear_icon.x + self.clear_icon.width and coords[1]*frame.shape[0] >= self.clear_icon.y and coords[1]*frame.shape[0] <= self.clear_icon.y + self.clear_icon.height
    
    def in_range_save(self, coords, frame):
        if not self.isOpen:
            return False
        return coords[0]*frame.shape[1] >= self.save_icon.x and coords[0]*frame.shape[1] <= self.save_icon.x + self.save_icon.width and coords[1]*frame.shape[0] >= self.save_icon.y and coords[1]*frame.shape[0] <= self.save_icon.y + self.save_icon.height    
    
    def clean(self):
        self.paint.clean_draw()
  
    def save(self):
        self.paint.save()
        
    def open(self):
        self.clear_icon.show()
        self.save_icon.show()
        self.isOpen = True       
    
    def close(self):
        self.clear_icon.hide()
        self.save_icon.hide()
        self.isOpen = False
        CloseAppEvent((0,0), Draw.__app_name)
        
    @classmethod
    def get(cls):
        if cls.__instance is None:
            raise Exception("Draw not initialized")
        return cls.__instance
    @classmethod
    def get_app_name(cls):
        return cls.__app_name
        
    
    