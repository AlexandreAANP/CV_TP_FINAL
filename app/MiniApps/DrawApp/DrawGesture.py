from Events.SelectEvent import SelectEvent
class DrawGesture():

    #return the coords and the gesture
    #1- if the gesture is a draw
    #2- if the gesture is clear
    def detect(self, landmarks) -> int or None:
        if landmarks is None or landmarks.right_hand_landmarks is None:
            return False
        fingers_up = SelectEvent.detect_which_finger_is_up(landmarks.right_hand_landmarks.landmark)
        gesture_position = self.__is_draw_gesture(fingers_up)
        if gesture_position:
            return (1,gesture_position)
        gesture_position = self.__is_clear_gesture(fingers_up)
        if gesture_position:
            return (2,gesture_position)
        return None
    
    def __is_clear_gesture(self, fingers_up: dict) -> tuple or None:
        if len(fingers_up) > 4:
            x =0
            y = 0
            i=0
            for finger in fingers_up.keys():
                if finger != "THUMB":
                    x += fingers_up[finger][0].x
                    y += fingers_up[finger][0].y
                    i+=1
            x = x/i
            y = y/i
            return (x,y)
        return None
    
    def __is_draw_gesture(self, fingers_up: dict) -> tuple or None:
        if len(fingers_up) <= 3 and "INDEX" in fingers_up.keys() and "MIDDLE" in fingers_up.keys():
            x = (fingers_up["INDEX"][0].x + fingers_up["MIDDLE"][0].x)/2
            y = (fingers_up["INDEX"][0].y + fingers_up["MIDDLE"][0].y)/2
            return (x,y)
        return None