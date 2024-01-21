from MiniApps.MiniApp import MiniApp
from Icon import Icon
from MiniApps.NinjaApp.Animation import Animation
from MiniApps.NinjaApp.AnimationFrame import AnimationFrame
from MiniApps.NinjaApp.CloseDetection import CloseDetection
from Events.CloseAppEvent import CloseAppEvent
from Events.SelectEvent import SelectEvent
import Utils
import cv2 as cv

class Ninja(MiniApp):
    __app_name = "Ninja"
    __instance = None
    ANIMATIONS = [("Orange01","Orange01_Mask"),
                  ("Orange02","Orange02_Mask"),
                  ("Orange03","Orange03_Mask"),
                  ("Orange04", "Orange04_Mask")]
    
    CACHE_PATH = Utils.PROJECT_PATH+"/MiniApps/NinjaApp/Ninja_cache/cache_file.pkl"
    ANIMATION_PATH = Utils.PROJECT_PATH+"/MiniApps/NinjaApp/Animations/"
    def __init__(self, width, height):
        super().__init__(Ninja.__app_name,
                         Icon(Utils.PROJECT_PATH+"/images/NinjaLogo.png",(0,45+Icon.HEIGHT*2+10), Ninja.__app_name))
        Ninja.__instance = self
        self.closeDetection = CloseDetection(2, width, height)
        self.width = width
        self.height = height
        self.isOpen = False
        self.animation = None
        self.animations = []
        self.right_hand_is_closed = False
        self.left_hand_is_closed = False
        self.pontuation = 0
        
        self.__generate_animation()
    
    def open(self):
        self.isOpen = True
    
    def close(self):
        self.isOpen = False
        self.pontuation = 0
        CloseAppEvent(None, Ninja.get_app_name())
    
    def run(self, landmarks, frame):
        if not self.isOpen:
            return frame
        # select random animation
        if not self.animation:
            self.animation = Animation.get_random_animation()
            self.animation.start()
        #check if is should close app
        if self.closeDetection.should_close(landmarks):
            self.animation.reset()
            self.animation = None
            self.close()
            return frame
        
        animation_frame = self.animation.next() # get next frame
        if not animation_frame:
            self.animation.reset() # reset animation
            self.animation = None
            frame = self.__put_pontuation_in_frame(frame)
            return frame
        
        frame = self.__put_animation_in_frame(animation_frame, frame)
        #to catch an object, the hand should be open before
        if self.__catch_animation_object(animation_frame, landmarks):
            #increment pontuation
            self.pontuation += 1
            #reset animation and put as None to next run() get other animation
            self.animation.reset()
            self.animation = None
        frame = self.__put_pontuation_in_frame(frame)                      
        return frame
    
    def __put_pontuation_in_frame(self, frame):
        frame = cv.flip(frame, 1)
        frame = cv.putText(frame, "Pontuation: "+str(self.pontuation), (0, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
        frame = cv.flip(frame, 1)
        return frame
    
    def __catch_animation_object(self, animationFrame: AnimationFrame, landsmarks):
        if not animationFrame:
            return False     
        if landsmarks.right_hand_landmarks:
            fingersUp = SelectEvent.detect_which_finger_is_up(landsmarks.right_hand_landmarks.landmark)
            if  len(fingersUp) <2:
                if self.right_hand_is_closed == False:
                    self.right_hand_is_closed = True
                    return self.__check_area_intersectation(self.__landmarks_area(landsmarks.right_hand_landmarks), animationFrame.start_end_points)
                else:
                    return False
            self.right_hand_is_closed = False
            return False
        if landsmarks.left_hand_landmarks:
            fingersUp = SelectEvent.detect_which_finger_is_up(landsmarks.left_hand_landmarks.landmark)
            if len(fingersUp) <2:
                if self.left_hand_is_closed == False:
                    self.left_hand_is_closed = True
                    return self.__check_area_intersectation(self.__landmarks_area(landsmarks.left_hand_landmarks), animationFrame.start_end_points)
                else:
                    return False
            return False
        return False
        
        
        
    def __landmarks_area(self, landmarks):
        if not landmarks:
            return None
        x = []
        y = []
        for point in landmarks.landmark:
            x.append(point.x)
            y.append(point.y)
        x_min = min(x) * self.width if min(x) * self.width > 0 else 0
        x_max = max(x) * self.width if max(x) * self.width < self.width else self.width
        y_min = min(y) * self.height if min(y) * self.height > 0 else 0
        y_max = max(y) * self.height if max(y) * self.height < self.height else self.height
        return ((int(x_min), int(y_min)), (int(x_max), int(y_max)))
       
    def __check_area_intersectation(self, a, b):
        # returns None if rectangles don't intersect
        dx = min(a[1][0], b[1][0]) - max(a[0][0], b[0][0])
        dy = min(a[1][1], b[1][1]) - max(a[0][1], b[0][1])
        if (dx>=0) and (dy>=0):
            return True
        return False   
    def __put_animation_in_frame(self, animation_frame: AnimationFrame, frame):
        if animation_frame:
            return Utils.replace_background_of_image(animation_frame.img, frame, animation_frame.mask)
        return frame
    
    def __generate_animation(self):
        for animation in Ninja.ANIMATIONS:
            self.animations.append(Animation(
                animation[0],
                Ninja.ANIMATION_PATH + animation[0] + "/",
                Ninja.ANIMATION_PATH + animation[1] + "/",
                self.width,
                self.height
            ))
    
    @classmethod
    def get_app_name(cls):
        return cls.__app_name
    @classmethod    
    def get(cls):
        if cls.__instance:
            return cls.__instance
        raise Exception("Ninja not initialized")    
    
    
    
    
    