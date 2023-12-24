from Events.Event import Event
class CloseDrawAppEvent(Event):
    def __init__(self, coords :tuple):
        super().__init__(coords, CloseDrawAppEvent)