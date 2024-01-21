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

def get_all_files_path_from_folder(path):
    import os
    images = []
    for filename in os.listdir(path):
        images.append(path+filename)
    return images

def area_of_shape(shape):
    return shape[0]*shape[1]

def distance_between_points(p1, p2):
    return int(((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5)

def distance_between_points_float(p1, p2, type="float"):
    return ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5

def middle_point(p1, p2):
    return (int((p1[0]+p2[0])/2), int((p1[1]+p2[1])/2))


def create_mask(img, BackgroundColor = (0,0,0)):
    import cv2 as cv
    if img.shape[2] < 4:
        img = cv.cvtColor(img, cv.COLOR_RGB2RGBA)
        for i in img[:, :, :]:
            for o in i:
                if o[0]==BackgroundColor[0] and o[1]==BackgroundColor[1] and o[2]==BackgroundColor[2]:
                    o[3] = 0
    ret, mask = cv.threshold(img[:, :, 3], 0, 255, cv.THRESH_BINARY)
    return mask

def replace_background_of_image(foreground, background, mask):
    
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

def detect_which_finger_is_up(landsmark):
        list_of_fingers_up = {
            #index: [points]
        }
        for index in cls.HAND.keys():
            finger = cls.HAND[index]
            isUp = True
            lastPoint = 0
            PointsList = []
            for key in finger[:-2]:
                PointsList.append(landsmark[key])
                if landsmark[key].y < lastPoint:
                    isUp = False
                    break
                lastPoint = landsmark[key].y
            if isUp:
                list_of_fingers_up[index] = PointsList
        return list_of_fingers_up