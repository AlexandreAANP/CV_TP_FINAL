import Colors
import cv2 as cv
import numpy as np
import datetime
import Utils
from Icon import Icon
class Paint():
    
    BUTTON_CLOSE_WIDTH = 35
    BUTTON_CLOSE_HEIGHT = 20
    
    def __init__(self, width, height, icons:list = []):
        self.icons = icons
        self.width = width
        self.height = height
        self.base_frame = self.__draw_base_background()
        self.paint = self.base_frame.copy()

        
    def get_draw(self):
        self.paint = self.__draw_nav_bar(self.paint)
        return self.paint.copy()
    def draw_point(self, coords, color):
        self.paint = cv.circle(self.paint, (int(coords[0]*self.paint.shape[1]), int(coords[1]*self.paint.shape[0])), 5, color, -1)
    
    def clean_point(self, coords):
        self.paint = cv.circle(self.paint, (int(coords[0]*self.paint.shape[1]), int(coords[1]*self.paint.shape[0])), 20, Colors.WHITE, -1)
    
    def clean_draw(self):
        self.paint = self.base_frame.copy()
        
    def save(self):
        saveImage = self.paint.copy()
        saveImage = self.__remove_nav_bar(saveImage)
        for icon in self.icons:
            saveImage = self.__remove_icon(icon, saveImage)
        saveImage = cv.flip(saveImage, 1)
        cv.imwrite(f'{Utils.PROJECT_PATH}/MiniApps/DrawApp/SavedDrawImages/image_saved_{str(datetime.datetime.now().strftime("%Y_%m_%d__%I_%M_%S_%p"))}.png', saveImage)
    
    def __remove_nav_bar(self, frame):
        frame = cv.rectangle(frame, (0,0), (frame.shape[1], 20), Colors.WHITE, -1)
        return frame
        
    def __remove_icon(self, icon:Icon, frame):
        frame = cv.rectangle(frame, (icon.x,icon.y), (icon.x+icon.width, icon.y+icon.height), Colors.WHITE, -1)
        return frame
    
    def __draw_base_background(self):
        base_frame = np.zeros((self.height, self.width, 3), np.uint8)
        base_frame = self.__draw_nav_bar(base_frame)
        base_frame = self.__draw_white_board(base_frame)
        return base_frame
    
    def __draw_nav_bar(self, frame):
        frame = cv.rectangle(frame, (0,0), (frame.shape[1], 20), Colors.GRAY, -1)
        frame = self.__draw_close_button(frame)
        return frame
    
    def __draw_close_button(self, frame):
        frame = cv.rectangle(frame, (0,0), (Paint.BUTTON_CLOSE_WIDTH, Paint.BUTTON_CLOSE_HEIGHT), Colors.RED, -1)
        frame = cv.putText(frame, "X", (15, 15), cv.FONT_HERSHEY_PLAIN, 0.7, (255, 255, 255), 1)
        return frame
    
    def __draw_white_board(self, frame):
        frame = cv.rectangle(frame, (0,20), (frame.shape[1], frame.shape[0]), (255,255,255), -1)
        return frame