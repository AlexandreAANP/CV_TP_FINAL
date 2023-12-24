from Events.EventsTrigger import EventsTrigger
class Event:    
    def __init__(self, coords :tuple, type):
        self.coords = coords
        self.type = type
        EventsTrigger.this.push(self)
        
