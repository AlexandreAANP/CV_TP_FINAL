import cv2 as cv
import mediapipe as mp
import numpy as np
from Utils import *
from MiniApps.MiniApp import MiniApp


def draw_landmarks(image, results):
    # Draw face connections
    mp_drawing.draw_landmarks(
        image,
        results.face_landmarks,
        mp_holistic.FACEMESH_CONTOURS,
        mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
        mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1),
    )
    # Draw pose connections
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(80, 22, 255), thickness=1, circle_radius=3),
        mp_drawing.DrawingSpec(color=(80, 44, 255), thickness=1, circle_radius=1),
    )
    # Draw left hand connections
    mp_drawing.draw_landmarks(
        image,
        results.left_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(255, 22, 76), thickness=1, circle_radius=3),
        mp_drawing.DrawingSpec(color=(255, 44, 250), thickness=1, circle_radius=1),
    )
    # Draw right hand connections
    mp_drawing.draw_landmarks(
        image,
        results.right_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(245, 255, 66), thickness=1, circle_radius=3),
        mp_drawing.DrawingSpec(color=(245, 255, 230), thickness=1, circle_radius=1),
    )


mp_holistic = mp.solutions.holistic  # Holistic model
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities
mediapipe_detection = lambda image: holistic.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
def testPoseLandmarks(landmark, frame):
    for index, i in enumerate(landmark):
        cv.putText(frame, str(index), (int(i.x*frame.shape[1]), int(i.y*frame.shape[0])), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        cv.circle(frame, (int(i.x*frame.shape[1]), int(i.y*frame.shape[0])), 5, (255, 0, 255), -1)

from Events.SelectEvent import SelectEvent
from Icon import Icon
from Events.EventsTrigger import EventsTrigger
from Events.EventsDetection import EventsDetection
from Controls import Controls
from MiniApps.DrawApp.Draw import Draw
from MiniApps.FaceReplaceApp.FaceReplace import FaceReplace
from MiniApps.AvoidObjects.AvoidObjects import AvoidObjects
if __name__ == "__main__":
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cap = cv.VideoCapture(0)
    _, frame = cap.read()
    AvoidObjects(
        dir_path+"/images/AvoidObjectsApp/Animations/animationsImages/",
        dir_path+"/images/AvoidObjectsApp/Animations/animationsImagesMask/",
        frame.shape[1], frame.shape[0])
    FaceReplace(
        dir_path+"/images/FaceReplaceApp/faces/",
        frame.shape[1],
        frame.shape[0])
    Draw(
        dir_path+"/images/Draw/newPage.png",
        dir_path+"/images/Draw/save.png",
        frame.shape[1],
        frame.shape[0])
    # Set mediapipe model
    with mp_holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))
        poseDetection = None
        while cv.pollKey() == -1:
            _, frame = cap.read()
            # Make detections
            testFrame = frame.copy()
            frameToShow = frame.copy()

            results = mediapipe_detection(frame)
            
            EventsDetection.get().detectEvents(results)
            draw_landmarks(testFrame, results)#TO REMOVE
            frameToShow = AvoidObjects.get().run(results, frameToShow)
            frameToShow = Draw.get().run(results, frameToShow)
            frameToShow = FaceReplace.get().run(results, frameToShow)
            #TODO DrawMouse replace the code below for that function
            coords = SelectEvent.detect(results.right_hand_landmarks)
            coords = coords.coords if coords is not None else None
            if coords:
                 cv.circle(frameToShow, (int(coords[0]*frameToShow.shape[1]), int(coords[1]*frameToShow.shape[0])), 5, (255, 0, 255), -1)
            #TO Remove
            if results.right_hand_landmarks:
                testPoseLandmarks(results.right_hand_landmarks.landmark, testFrame) #TO REMOVE
            #TO REMOVE
            if results.left_hand_landmarks is not None:
                testPoseLandmarks(results.left_hand_landmarks.landmark, testFrame) #TO REMOVE
            
            #cv.imshow("Frame", frame)
            
            cv.imshow("TestFrame", testFrame)
            
            for icon in MiniApp.getAllAppIcons():
                icon.putImageInFrame(frameToShow)
            
            
            
            Controls.get().checkEvents(frameToShow)
            #Should be the last command
            frameToShow = cv.flip(frameToShow, 1)
            frameToShow = cv.resize(frameToShow, (0, 0), fx=1.5, fy=1.5)
            cv.imshow("FrameToShow", frameToShow)
            
            
            