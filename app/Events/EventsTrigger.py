class EventsTrigger():
    instance = None
    def __init__(self):
        self.__events = []
        self.length = 0
        EventsTrigger.instance = self
        
    def push(self, event):
        if event is None:
            return
        self.__events.append(event)
        self.length +=1
        
    def pop(self):
        event = self.__events.pop(0)
        self.length -=1
        return event
    
    @classmethod
    def get(cls):
        if not EventsTrigger.instance:
            EventsTrigger.instance = EventsTrigger()
        return EventsTrigger.instance  