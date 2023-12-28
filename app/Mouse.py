
import Utils
import cv2 as cv
from Events.SelectEvent import SelectEvent
class Mouse:
    WIDTH = 20
    HEIGTH = 20
    __instance = None
    PATH_ICON = "/images/mouse.png"
    def __init__(self):
        self.__instance = self
        self.icon_image_mask = Utils.CreateMask(
            cv.flip(
                cv.resize(
                cv.imread(Utils.PROJECT_PATH+Mouse.PATH_ICON, cv.IMREAD_UNCHANGED),
                (Mouse.WIDTH, Mouse.HEIGTH)
            ),1))
        self.icon_image = cv.flip(cv.resize(
            cv.imread(
                Utils.PROJECT_PATH+Mouse.PATH_ICON),
                (Mouse.WIDTH, Mouse.HEIGTH)
            ),1)
      
    @classmethod
    def get(cls):
        if not Mouse.__instance:
            Mouse.__instance = Mouse()
        return Mouse.__instance    
    def run(self, landsmarks, frame):
        if not landsmarks:
            return frame
        select_event = SelectEvent.detect(landsmarks)
        if select_event:
            x = int(select_event.coords[0] * frame.shape[1])-Mouse.WIDTH
            y = int(select_event.coords[1] * frame.shape[0])
            w,h =(Mouse.WIDTH, Mouse.HEIGTH)
            if x<0 or y < 0:
                return frame
            print(x,y,w,h)
            if x<frame.shape[1] and x+w > frame.shape[1]:
                w = frame.shape[1] - x
            if y<frame.shape[0] and y+h > frame.shape[0]:
                h = frame.shape[0] - y
            
            if x+w > frame.shape[1] or y+h > frame.shape[0]:
                return frame
            print(x,y,w,h)
            part_of_frame = frame[y:y+h,x:x+w]
            icon = self.icon_image[:h, :w]
            mask = self.icon_image_mask[:h, :w]
            print(part_of_frame.shape, icon.shape, mask.shape) 
            frame[y:y+h,x:x+w] = Utils.replaceBackgroundOfImage(icon, part_of_frame, mask)
        return frame