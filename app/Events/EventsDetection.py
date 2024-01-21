from Events.SelectEvent import SelectEvent
from Events.EventsTrigger import EventsTrigger
class EventsDetection:
    instance = None
    def __init__(self):
        self.instance = self
        self.eventTrigger = EventsTrigger.get()
    
        
    def detect_events(self, landmarks):
        if landmarks is None:
            return
        SelectEvent.detect(landmarks.right_hand_landmarks)
        SelectEvent.detect(landmarks.left_hand_landmarks)
        
    @classmethod
    def get(cls):
        if not EventsDetection.instance:
            EventsDetection.instance = EventsDetection()
        return EventsDetection.instance  
        
    
    