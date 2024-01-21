import abc
from Icon import Icon
class MiniApp (abc.ABC):
    Apps = []
    def __init__(self, name, icon: Icon):
        self.name = name
        self.icon = icon
        self.is_open = False
        MiniApp.Apps.append(self)

    @classmethod
    @abc.abstractmethod
    def get(cls):
        pass
    
    @abc.abstractmethod
    def run(self, landsmarks, frame):
        if not self.is_open:
            return frame
        pass

    @abc.abstractmethod
    def open(self):
        pass
    
    @abc.abstractmethod
    def close(self):
        pass
    
    @classmethod
    @abc.abstractmethod
    def get_app_name(self):
        pass
    
    @classmethod
    def run_apps(cls, landmarks, frame):
        if not cls.which_app_is_open():
            return frame
        
        return cls.__which_app_is_open().run(landmarks, frame)

    @classmethod
    def get_all_app_icons(cls):
        return list(map(lambda app: app.icon, cls.Apps))
    
    @classmethod
    def open_app(cls,appName: str) -> bool or Exception:
        for app in cls.Apps:
            app.icon.hide()
            if app.name == appName:
                app.open()
                return True
        raise Exception("App not found")
    
    @classmethod
    def close_all_app_icons(cls):
        for icon in cls.get_all_app_icons():
            icon.hide()
    
    @classmethod
    def which_app_is_open(cls) -> str:
        for app in cls.Apps:
            if app.isOpen:
                return app.name
        else:
            return None
    @classmethod
    def __which_app_is_open(cls):
        for app in cls.Apps:
            if app.isOpen:
                return app
        else:
            return None
    @classmethod
    def close_all_apps(cls):
        for icon in cls.get_all_app_icons():
            icon.show()
        
    
    @classmethod
    def get_app_by_icon(cls, icon :Icon):
        for app in cls.Apps:
            if app.icon == icon:
                return app.name
        return None    
    

