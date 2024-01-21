from Events.SelectEvent import SelectEvent
import time
class CloseDetection:
    def __init__(self, seconds_to_close:int, width:int, height:int):
        self.timer = None
        self.seconds_to_close = seconds_to_close
        self.width = width
        self.height = height
    
    def should_close(self, landmarks):
        if not landmarks or not landmarks.right_hand_landmarks:
            return False
        if self.__is_gesture_to_close(landmarks):
            if not self.timer:
                self.timer = time.time()
            else:
                if time.time() - self.timer > self.seconds_to_close:
                    self.timer = None
                    return True
    
    def __is_gesture_to_close(self, landmarks):
        fingers_up = SelectEvent.detect_which_finger_is_up(landmarks.right_hand_landmarks.landmark)  
        if len(fingers_up) == 4 and not "INDEX" in fingers_up:
            return True
        return False

    