from Events.Event import Event
class OpenDrawAppEvent(Event):
    def __init__(self, coords :tuple):
        super().__init__(coords, OpenDrawAppEvent)