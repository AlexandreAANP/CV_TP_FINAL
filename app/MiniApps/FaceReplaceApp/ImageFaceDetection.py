import cv2 as cv
import Utils
import mediapipe as mp
class ImageFaceDetection():
    
    MODEL = mp.solutions.holistic.Holistic(
             min_detection_confidence=0.5, min_tracking_confidence=0.5
            )
    def __init__(self, path):
        self.image = cv.imread(path)
        self.results = self.__mediapipe_detection(self.image)
        if self.results.face_landmarks is None:
                raise Exception("No face detected")
        self.mask = Utils.create_mask(cv.imread(path, cv.IMREAD_UNCHANGED))
        self.categorized_face_points = self.__categorized_face_points(self.results.face_landmarks.landmark)
        
    def replaceFace(self, landmarks, frame):
        if(landmarks.face_landmarks is None): return frame
        
        coords, shape = self.__get_coords_square_shape(landmarks.face_landmarks.landmark, frame)
        
        face,mask = self.__resize_face(shape[1],shape[0])
        coordNose = landmarks.face_landmarks.landmark[Utils.NOSE_CENTER]#coords from landmarks
        coordsNoseFace = self.__coords_relative_frame(coords, face.shape)#coords from face img
        

        # #difference between coords from landmarks and coords from face img
        x = int((coordNose.x * frame.shape[1]) - coordsNoseFace[0])
        y = int((coordNose.y * frame.shape[0]) - coordsNoseFace[1])
        #replace to the new coords
        coords = (coords[0]+x, coords[1]+y)
        
        #size of the face
        newShape = self.__size_from_face_porportion(frame, landmarks)
        face,mask = self.__resize_face(newShape[1],newShape[0])
        part_of_frame = frame[coords[1]:coords[1]+newShape[0], coords[0]:coords[0]+newShape[1]]
        if part_of_frame.shape[0] != face.shape[0] or part_of_frame.shape[1] != face.shape[1]:
            return frame
        frame[coords[1]:coords[1]+newShape[0], coords[0]:coords[0]+newShape[1]] = Utils.replace_background_of_image(face, part_of_frame, mask)
        return frame
    
    
    def __size_from_face_porportion(self, frame, results):
        #distance between eyes = 3/5 of the width of the face, the height is porporcional to the width
        width = int((self.__horizontal_distance_from_eyes(frame,results)*5)/3)
        height = int((self.image.shape[0]*width)/self.image.shape[1])
        return (height,width)
    
    def __horizontal_distance_from_eyes(self, frame, results):
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
        return Utils.distance_between_points(Lp, Rp)
    
    def __coords_relative_frame(self, coords, shape):
        x = self.categorized_face_points["nose_center"][0].x * shape[1]
        y = self.categorized_face_points["nose_center"][0].y * shape[0]
        return (coords[0]+x, coords[1]+y)
    
    def __resize_face(self, width, height):
        face = cv.resize(self.image, (width, height)).copy()
        mask = cv.resize(self.mask, (width, height)).copy()
        return (face,mask)   
    
    def __get_coords_square_shape(self, landmarks, image):
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
        
        return (v1,(Utils.distance_between_points(v1,v3),Utils.distance_between_points(v1,v2)))
                
    def __categorized_face_points(self, face_landmarks):
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
    
    __mediapipe_detection = lambda self, image: ImageFaceDetection.MODEL.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))