class EventsTrigger():
    this = None
    def __init__(self):
        self.__events = []
        self.__previuosEvents = []
        self.length = 0
        EventsTrigger.this = self
        
    def push(self, event):
        if event is None:
            return
        self.__events.append(event)
        self.length +=1
        
    def pop(self):
        event = self.__events.pop(0)
        self.__previuosEvents.append(event)
        self.length -=1
        return event