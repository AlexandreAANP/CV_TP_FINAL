from Events.Event import Event
class CloseAppEvent(Event):
    def __init__(self, coords :tuple, app_name :str):
        super().__init__(coords, CloseAppEvent)
        self.app_name = app_name