from Events.Event import Event
class OpenAppEvent(Event):
    def __init__(self, coords :tuple, app_name :str):
        super().__init__(coords, OpenAppEvent)
        self.app_name = app_name