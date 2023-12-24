from Events.SelectEvent import SelectEvent
from Events.EventsTrigger import EventsTrigger
class EventsDetection:
    def __init__(self, landmarks):
        self.lanfmarks = landmarks
        self.eventTrigger = EventsTrigger.this
        self.detectEvents()
        
    def detectEvents(self):
        #TODO
        self.eventTrigger.push(SelectEvent.detect(self.lanfmarks.right_hand_landmarks))
        self.eventTrigger.push(SelectEvent.detect(self.lanfmarks.left_hand_landmarks))
        pass
    
    