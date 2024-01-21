from Events.Event import Event
import time
import abc
class EventInteraction(abc.ABC):
    SECONDS_TO_TRIGGER_EVENT = 2
    def __init__(self):
        self.timer = None
        self.event_type = None
        
    def should_trigger_event(self, event :Event):
        if self.timer and self.event_type == event.type:
            if time.time() - self.timer > self.SECONDS_TO_TRIGGER_EVENT:
                self.timer = None
                return True
            else:
                return False
        else:
            self.timer = time.time()
            self.event_type = event.type
            return False
        
    def reset_event(self):
        self.timer = None
        self.event_type = None
        
    @abc.abstractmethod
    def event(self, event:Event, frame):
        pass