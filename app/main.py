import cv2 as cv
import mediapipe as mp
from MiniApps.MiniApp import MiniApp
from MiniApps.NinjaApp.Ninja import Ninja
from MiniApps.FaceReplaceApp.FaceReplace import FaceReplace
from MiniApps.DrawApp.Draw import Draw
from Events.EventsDetection import EventsDetection
from Controls import Controls
from Mouse import Mouse

mp_holistic = mp.solutions.holistic  # Holistic model
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities
mediapipe_detection = lambda image: holistic.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    _, frame = cap.read()
    Mouse()
    Ninja(frame.shape[1], frame.shape[0])
    FaceReplace(frame.shape[1], frame.shape[0])
    Draw(frame.shape[1],frame.shape[0])
    
    # Set mediapipe model
    with mp_holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:
        while cv.pollKey() == -1:
            _, frame = cap.read()

            results = mediapipe_detection(frame)
            
            EventsDetection.get().detectEvents(results)
            
            frame = MiniApp.run_apps(results, frame)

            frame = Mouse.get().run(results.right_hand_landmarks, frame)

            for icon in MiniApp.get_all_app_icons():
                icon.putImageInFrame(frame)
            
            
            
            Controls.get().check_events(frame)
            
            #Should be the last command
            frame = cv.flip(frame, 1)
            frame = cv.resize(frame, (0, 0), fx=1.5, fy=1.5)
            cv.imshow("CV_TP_FINAL v.1", frame)
            
            
            