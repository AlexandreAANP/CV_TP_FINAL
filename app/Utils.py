import numpy as np
import cv2 as cv
import os
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
# Left eyes indices 
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
LEFT_EYEBROW =[ 336, 296, 334, 293, 300, 276, 283, 282, 295, 285 ]

# right eyes indices
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]  
RIGHT_EYEBROW=[ 70, 63, 105, 66, 107, 55, 65, 52, 53, 46 ]

#Nose center Indice
NOSE_CENTER = 1

RIGHT_SHOULDER = 12
RIGTH_ELBOW = 14
RIGTH_WIRST = 16

LEFT_SHOULDER = 11
LEFT_ELBOW = 13
LEFT_WIRST = 15

def getAllFilesPathFromFolder(path):
    import os
    images = []
    for filename in os.listdir(path):
        images.append(path+filename)
    return images

def areaOfShape(shape):
    return shape[0]*shape[1]

def ThereIsMoviment(oldPoint, newPoint, threshold=5):
    differenceX = oldPoint[0]-newPoint[0] if oldPoint[0]-newPoint[0] > 0 else -1*(oldPoint[0]-newPoint[0])
    differenceY = oldPoint[1]-newPoint[1] if oldPoint[1]-newPoint[1] > 0 else -1*(oldPoint[1]-newPoint[1])
    if differenceX > threshold or differenceY > threshold:
        return True
    return False

def distanceBetweenPoints(p1, p2):
    return int(((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5)

def distanceBetweenPointsFloat(p1, p2, type="float"):
    return ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5

def middlePoint(p1, p2):
    return (int((p1[0]+p2[0])/2), int((p1[1]+p2[1])/2))

# def ThereIsMoviment(frame1, frame2, area=500):
#     import cv2 as cv
#     frame1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
#     frame2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
#     frame1 = cv.GaussianBlur(frame1, (21, 21), 0)
#     frame2 = cv.GaussianBlur(frame2, (21, 21), 0)
#     frameDelta = cv.absdiff(frame1, frame2)
#     thresh = cv.threshold(frameDelta, 25, 255, cv.THRESH_BINARY)[1]
#     thresh = cv.dilate(thresh, None, iterations=2)
#     cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,
#         cv.CHAIN_APPROX_SIMPLE)
    
#     for c in cnts:
#         if cv.contourArea(c) > area:
#             return True

def CreateMask(img, BackgroundColor = (0,0,0)):
    import cv2 as cv
    if img.shape[2] < 4:
        img = cv.cvtColor(img, cv.COLOR_RGB2RGBA)
        for i in img[:, :, :]:
            for o in i:
                if o[0]==BackgroundColor[0] and o[1]==BackgroundColor[1] and o[2]==BackgroundColor[2]:
                    o[3] = 0
                else:
                    print(o)
    ret, mask = cv.threshold(img[:, :, 3], 0, 255, cv.THRESH_BINARY)
    return mask

def replaceBackgroundOfImage(foreground, background, mask):
    
    # First create the image with alpha channel
    
    # Convert uint8 to float
    foreground = foreground.astype(float)
    background = background.astype(float)

    # Normalize the mask mask to keep intensity between 0 and 1
    mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
    mask = mask.astype(float) / 255

    # Multiply the foreground with the mask matte
    foreground = cv.multiply(mask, foreground)

    # Multiply the background with ( 1 - mask )
    background = cv.multiply(1.0 - mask, background)

    # Add the masked foreground and background.
    return cv.add(foreground, background).astype(np.uint8)

# def drawEye(results, frame):
#     points = results.face_landmarks.landmark
#     for num, i in enumerate(points):
#         if num in LEFT_EYE:
#             cv.circle(frame, (int(i.x*frame.shape[1]), int(i.y*frame.shape[0])), 5, (255, 0, 255), 5)
#     return frame

def drawOnlyThePerimeter(image, results, round_n_digits=2):
    points = results.left_hand_landmarks.landmark
    LeftExtermities = {}
    RightExtermities = {}
    for i in points:
        x = i.x
        y = i.y
        yRounded = round(i.y, round_n_digits)
        if(str(yRounded) in LeftExtermities.keys()):
            if(x < LeftExtermities[str(yRounded)][0]):
                LeftExtermities[str(yRounded)] = (x,y)
        else:
            LeftExtermities[str(yRounded)] = (x,y)
        if(str(yRounded) in RightExtermities.keys()):
            if(x > RightExtermities[str(yRounded)][0]):
                RightExtermities[str(yRounded)] = (x,y)
        else:
            RightExtermities[str(yRounded)] = (x,y)
    
    for i in LeftExtermities.keys():
        cv.circle(image, (int(LeftExtermities[i][0]*image.shape[1]), int(LeftExtermities[i][1]*image.shape[0])), 1, (0, 0, 255), -1) 
    
    for i in RightExtermities.keys():
        cv.circle(image, (int(RightExtermities[i][0]*image.shape[1]), int(RightExtermities[i][1]*image.shape[0])), 1, (0, 0, 255), -1)       



# def drawSquareForEach(image, results):
#     points = results.face_landmarks.landmark
#     for i in points:
#         print(i.x, i.y)
#         cv.circle(image, (int(i.x*image.shape[1]), int(i.y*image.shape[0])), 5, (0, 0, 255), -1)
# def ThereIsMoviment2(frame1, frame2, difference=100):
#     import cv2 as cv
#     frame1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
#     frame2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
#     frame1 = cv.GaussianBlur(frame1, (21, 21), 0)
#     frame2 = cv.GaussianBlur(frame2, (21, 21), 0)
    
#     #The smaller shape will be the shape of both
#     shape = [0,0]
#     if frame1.shape[0] <= frame2.shape[0]:
#         shape[0] = frame1.shape[0]
#     else:
#         shape[0] = frame2.shape[0]
#     if frame1.shape[1] <= frame2.shape[1]:
#         shape[1] = frame1.shape[1]
#     else:
#         shape[1] = frame2.shape[1]
#     print(shape)
#     frameDelta = cv.absdiff(frame1[:shape[0], :shape[1]], frame2[:shape[0], :shape[1]])
#     thresh = cv.threshold(frameDelta, 25, 255, cv.THRESH_BINARY)[1]
#     thresh = cv.dilate(thresh, None, iterations=2)
#     cnts, _ = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
#     for c in cnts:
#         (x, y, w, h) = cv.boundingRect(c)
#         if w > difference or h > difference:
#             print(True)
#             return True
#     print(False)    
#     return False