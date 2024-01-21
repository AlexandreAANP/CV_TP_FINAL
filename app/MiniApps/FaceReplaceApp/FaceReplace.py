import Utils
import cv2 as cv
import mediapipe as mp
from Icon import Icon
from MiniApps.MiniApp import MiniApp
from Events.SelectEvent import SelectEvent
import time
mp_holistic = mp.solutions.holistic
mediapipe_detection = lambda image: holistic.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
import os
class FaceReplace(MiniApp):
    __app_name = "FaceReplaceApp"
    __instance = None
    PATH = os.path.dirname(os.path.realpath(__file__)).replace("\MiniApps\FaceReplaceApp", "")
    
    PATH_ARROW_ICON = PATH+"\\images\\FaceReplaceApp\\arrow.png"
    
    def __init__(self, path: str, width, height):
        FaceReplace.__instance = self
        super().__init__(FaceReplace.__app_name,
                         Icon(Utils.PROJECT_PATH+"/images/obama.png",(0,45), FaceReplace.__app_name))
        listPathReplaceFace = Utils.getAllFilesPathFromFolder(path)
        self.rigth_icon = Icon(FaceReplace.PATH_ARROW_ICON, (0,int(height/2 - Icon.HEIGHT/2)), "FaceReplaceApp_Arrow_Left", flip = True)
        self.left_icon = Icon(FaceReplace.PATH_ARROW_ICON, (width-70,int(height/2 - Icon.HEIGHT/2)), "FaceReplaceApp_Arrow_Rigth", flip=False)
        self.faces_landsmarks = []
        self.CategorizedFacePointsList = []
        self.faces = []
        self.facesMasks = []
        with mp_holistic.Holistic(
             min_detection_confidence=0.5, min_tracking_confidence=0.5
            ) as holistic:
            for path in listPathReplaceFace:
                img = cv.imread(path)
                self.results = holistic.process(img)
                if self.results.face_landmarks is None:
                    print(path, "no face detected")
                    continue #no face detected
                self.faces_landsmarks.append(self.results.face_landmarks)
                self.CategorizedFacePointsList.append(self.CategorizedFacePoints(self.results.face_landmarks.landmark))
                self.faces.append(img)
                self.facesMasks.append(Utils.CreateMask(cv.imread(path, cv.IMREAD_UNCHANGED)))
        self.faceNumber = len(self.faces)
        self.faceIndex = 0
        self.isOpen = False
    @classmethod  
    def get(cls):
        if cls.__instance:
            return cls.__instance
        raise Exception("FaceReplaceApp not initialized")
    
    @classmethod
    def get_app_name(cls):
        return cls.__app_name
    
    def changeFace(self, direction):
        if direction == "left":
            self.faceIndex -= 1 if self.faceIndex > 0 else 0
            return True
        elif direction == "right":
            self.faceIndex += 1 if self.faceIndex < self.faceNumber-1 else 0
            return True
        return False
    
    def inRangeLeftIcon(self, coords, frame):
        return self.left_icon.inRange(coords, frame)
    def inRangeRightIcon(self, coords, frame):
        return self.rigth_icon.inRange(coords, frame)
            
    def is_gesture_to_close(self, landmarks, frame):
        if not landmarks or not landmarks.right_hand_landmarks:
            return False
        fingers_up = SelectEvent.detectWhichFingerIsUp(landmarks.right_hand_landmarks.landmark)  
        if len(fingers_up) == 4 and not "INDEX" in fingers_up:
            return True
        return False
            
    def start_time(self):
        if self.start is None:
            self.start = time.time()
        
    def reset_time(self):
        self.start = None
        
        
    def run(self,landmarks,frame):
        if not self.isOpen:
            return frame
        self.rigth_icon.putImageInFrame(frame)
        self.left_icon.putImageInFrame(frame)
        #Check exit
        if self.is_gesture_to_close(landmarks, frame):
            print("Closing FaceReplaceApp")
            self.start_time()
            if time.time() - self.start > 2:
                self.reset_time()
                MiniApp.CloseAllApps()
                return frame
        else:
            self.reset_time()
        if landmarks is None or landmarks.face_landmarks is None:
            return frame

        coords, shape = self.getCoordsAndSquareShape(landmarks.face_landmarks.landmark, frame)
        
        face,mask = self.resizeFace(shape[1],shape[0])
        coordNose = landmarks.face_landmarks.landmark[Utils.NOSE_CENTER]#coords from landmarks
        coordsNoseFace = self.coordsRelativeOfFrame(coords, face.shape)#coords from face img
        #difference between coords from landmarks and coords from face img
        x = int((coordNose.x * frame.shape[1]) - coordsNoseFace[0])
        y = int((coordNose.y * frame.shape[0]) - coordsNoseFace[1])
        #replace to the new coords
        coords = (coords[0]+x, coords[1]+y)
        
        #size of the face
        newShape = self.sizeFromFacePorportion(frame, landmarks, self.faces[self.faceIndex])
        face,mask = self.resizeFace(newShape[1],newShape[0])
        partOfFrame = frame[coords[1]:coords[1]+newShape[0], coords[0]:coords[0]+newShape[1]]
        if partOfFrame.shape[0] != face.shape[0] or partOfFrame.shape[1] != face.shape[1]:
            return frame
        frame[coords[1]:coords[1]+newShape[0], coords[0]:coords[0]+newShape[1]] = Utils.replaceBackgroundOfImage(face, partOfFrame, mask)
        
        
        return frame
    
    def sizeFromFacePorportion(self, frame, results, img):
        #distance between eyes = 3/5 of the width of the face, the height is porporcional to the width
        width = int((self.horizontalDistanceFromEyes(frame,results)*5)/3)
        height = int((img.shape[0]*width)/img.shape[1])
        return (height,width)
    
    def coordsRelativeOfFrame(self, coords, shape):
        x = self.CategorizedFacePointsList[self.faceIndex]["nose_center"][0].x * shape[1]
        y = self.CategorizedFacePointsList[self.faceIndex]["nose_center"][0].y * shape[0]
        return (coords[0]+x, coords[1]+y)

    def CategorizedFacePoints(self, face_landmarks):
        res = {
            "left_eye": [],
            "left_eyebrow": [],
            "right_eye": [],
            "right_eyebrow": [],
            "nose_center":[]
        }
        for index, point in enumerate(face_landmarks):
            if index in Utils.LEFT_EYE:
                res["left_eye"].append(point)
            elif index in Utils.LEFT_EYEBROW:
                res["left_eyebrow"].append(point)
            elif index in Utils.RIGHT_EYE:
                res["right_eye"].append(point)
            elif index in Utils.RIGHT_EYEBROW:
                res["right_eyebrow"].append(point)
            elif index == Utils.NOSE_CENTER:
                res["nose_center"].append(point)
        return res
    
    def horizontalDistanceFromEyes(self, frame, results):
        # (         )
        # ( *<--->* )
        # (    v    )
        points = results.face_landmarks.landmark
        LeftPoint = (0,0)
        RightPoint = (1,0)
        for num, i in enumerate(points):
            if num in Utils.LEFT_EYE:
                if  i.x > LeftPoint[0]:
                    LeftPoint = (i.x, i.y)
            elif num in Utils.RIGHT_EYE:
                if i.x < RightPoint[0]:
                    RightPoint = (i.x, i.y)

        
        Rp = (int(RightPoint[0]*frame.shape[1]), int(RightPoint[1]*frame.shape[0]))
        Lp = (int(LeftPoint[0]*frame.shape[1]), int(LeftPoint[1]*frame.shape[0]))
        return Utils.distanceBetweenPoints(Lp, Rp)
    
    def sizeFromFacePorportion(self, frame, results, img):
        #distance between eyes = 3/5 of the width of the face, the height is porporcional to the width
        width = int((self.horizontalDistanceFromEyes(frame,results)*5)/3)
        height = int((img.shape[0]*width)/img.shape[1])
        return (height,width)
    
    def resizeFace(self, width, height):
        face = cv.resize(self.faces[self.faceIndex], (width, height)).copy()
        mask = cv.resize(self.facesMasks[self.faceIndex], (width, height)).copy()
        return (face,mask)
        
    
    def getCoordsAndSquareShape(self, landmarks, image):
        if(landmarks is None): return None
        points = landmarks
        # ---p1---
        # |      |
        # p2     p3
        # |      |
        # ---p4---
        p1,p2,p3,p4 = [1,1],[1,1],[0,0],[0,0]
        for i in points:
            x = i.x
            y = i.y
            if(y < p1[1]):
                p1[0] = x
                p1[1] = y 
            if(x < p2[0]):
                p2[0] = x
                p2[1] = y
            if(x > p3[0]):
                p3[0] = x
                p3[1] = y
            if(y > p4[1]):
                p4[0] = x
                p4[1] = y
            
        #Get Vertices
        # v1----v2
        # |      |
        # v3----v4
        v1 = [int(p2[0]*image.shape[1]), int(p1[1]*image.shape[0])]
        v2 = [int(p3[0]*image.shape[1]), int(p1[1]*image.shape[0])]
        v3 = [int(p2[0]*image.shape[1]), int(p4[1]*image.shape[0])]
        v4 = [int(p3[0]*image.shape[1]), int(p4[1]*image.shape[0])]
        for vertice in [v1,v2,v3,v4]:
            if vertice[0] < 0:
                vertice[0] = 0
            if vertice[0] > image.shape[1]:
                vertice[0] = image.shape[1]
            if vertice[1] < 0:
                vertice[1] = 0
            if vertice[1] > image.shape[0]:
                vertice[1] = image.shape[0]
        v1 = tuple(v1)
        v2 = tuple(v2)
        v3 = tuple(v3)
        v4 = tuple(v4)
        
        return (v1,(Utils.distanceBetweenPoints(v1,v3),Utils.distanceBetweenPoints(v1,v2)))
    
    def open(self):
        self.isOpen = True
    
    def close(self):
        self.isOpen = False
        
