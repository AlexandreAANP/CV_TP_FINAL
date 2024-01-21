from MiniApps.NinjaApp.AnimationFrame import AnimationFrame
import Utils
import cv2 as cv
import pickle
import random
class Animation():
    
    CACHE_PATH = Utils.PROJECT_PATH+"/MiniApps/NinjaApp/Ninja_cache/"
    ANIMATIONS = []
    def __init__(self, name:str, path_images:str, path_mask:str, width:int, height:int):
        print(width,height)
        for animation in Animation.ANIMATIONS:
            if animation.name == name:
                raise Exception(f"Animation with name {name} already exists")
        Animation.ANIMATIONS.append(self)

        self.name = name
        self.paths = (path_images, path_mask)
        self.width = width
        self.height = height
        self.frames = []
        self.index = 0
        self.__is_running = False
        self.__loop_animation = False
        
        self.__load_animation()
        
    def next(self) -> AnimationFrame or None:
        if not self.__is_running:
            return
        if self.index >= len(self.frames):
            self.__is_running = False
            if self.__loop_animation:
                self.index = 0
                return self.frames[self.index]
            return
        frame = self.frames[self.index]
        self.index += 1
        return frame
    
    def get(self) -> AnimationFrame:
        return self.frames[self.index]
    
    def is_running(self):
        return self.__is_running
    
    def set_animation_loop(self, loop:bool):
        self.__loop_animation = loop
            
    def stop(self):
        self.__is_running = False
    
    def start(self):
        self.__is_running = True
    
    def reset(self):
        self.index = 0
    
    @classmethod
    def is_animation_running(cls):
        for animation in cls.ANIMATIONS:
            if animation.is_running():
                return True
        return False
    @classmethod
    def which_animation_is_running(cls):
        for animation in cls.ANIMATIONS:
            if animation.is_running():
                return animation
        return None
    
    @classmethod
    def start_animation(cls, name:str):
        for animation in cls.ANIMATIONS:
            if animation.name == name:
                animation.start()
            else:
                animation.stop()
    @classmethod
    def stop_animation(cls, name:str):
        for animation in cls.ANIMATIONS:
            if animation.name == name:
                animation.stop()
        
    @classmethod
    def get_random_animation(cls):
        return cls.ANIMATIONS[random.randint(0, len(cls.ANIMATIONS)-1)]
    def __load_animation(self, from_cache:bool=True):
        if from_cache:
            if not self.__try_load_from_cache():
                print("Could not load from cache")
                self.__load_from_images()
        else:
            self.__load_from_images()
            
    def __load_from_images(self, cache_files:bool=True):
        images = []
        mask = []
        start_end_points = []
        path_animation, path_animation_mask = self.paths
        
        for path in Utils.getAllFilesPathFromFolder(path_animation):
            images.append(cv.resize(cv.imread(path),(self.width, self.height)))
            
        for path in Utils.getAllFilesPathFromFolder(path_animation_mask):
            _mask = cv.resize(cv.imread(path, cv.THRESH_BINARY),(self.width, self.height))
            mask.append(_mask)
            start_point, end_point = self.__calculate_object_shape(_mask)
            start_end_points.append((start_point, end_point))
        
        for i,img in enumerate(images):
            self.frames.append(AnimationFrame(
                                              i,
                                              img,
                                              mask[i],
                                              start_end_points[i]))
        
        if cache_files:
            self.__cache_animation()
                
    
    def __try_load_from_cache(self):
        try:
            with open(Animation.CACHE_PATH+self.name+".pkl", "rb") as file:
                self.frames = pickle.load(file)
            return True
        except Exception as e:
            return False
    
    def __cache_animation(self):
        with open(Animation.CACHE_PATH+self.name+".pkl", "wb") as file:
            pickle.dump(self.frames, file)
    
    def __calculate_object_shape(self, mask):
        y_list = []
        x_list = []
        for y,line in enumerate(mask):
            flag = False
            for x,value in enumerate(line):
                if value != 0:
                    flag = True
                    y_list.append(y)
                    x_list.append(x)
                elif flag:
                    break
        if len(x_list) == 0:
            x_list.append(0)
            x_list.append(mask.shape[1])
        if len(y_list) == 0:
            y_list.append(0)
            y_list.append(mask.shape[0])
        return ((min(x_list),min(y_list)),(max(x_list),max(y_list)))
        
        
