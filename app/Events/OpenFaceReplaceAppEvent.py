from Events.Event import Event
class OpenFaceReplaceAppEvent(Event):
    def __init__(self, coords :tuple):
        super().__init__(coords, OpenFaceReplaceAppEvent)