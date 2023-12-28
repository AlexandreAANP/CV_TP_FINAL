import abc
from Icon import Icon

class MiniApp (abc.ABC):
    Apps = []
    def __init__(self, name, icon: Icon):
        self.name = name
        self.icon = icon
        self.isOpen = False
        MiniApp.Apps.append(self)


    @classmethod
    def getAllAppIcons(cls):
        return list(map(lambda app: app.icon, cls.Apps))
    
    @classmethod
    @abc.abstractmethod
    def get(cls):
        pass
    
    @classmethod
    def OpenApp(cls,appName: str):
        flag = False
        for app in cls.Apps:
            if app.name == appName:
                flag = True
        if not flag:
            raise Exception("App not found")
        for app in cls.Apps:
            from MiniApps.FaceReplaceApp.FaceReplace import FaceReplace
            app.icon.hide() if app.name != FaceReplace.get_app_name() else app.icon.show()
            if app.name == appName:
                app.open()
            else:
                app.close()
        
        map(lambda icon: icon.hide(), cls.getAllAppIcons())
        return True
    
    @classmethod
    def which_app_is_open(cls) -> str:
        for app in cls.Apps:
            if app.isOpen:
                return app.name
        else:
            return None
    
    @classmethod
    def CloseAllApps(cls):
        for app in cls.Apps:
            app.close()
        for icon in cls.getAllAppIcons():
            icon.show()
        
    
    @classmethod
    def get_app_by_icon(cls, icon :Icon):
        for app in cls.Apps:
            if app.icon == icon:
                return app.name
        return None    
    @classmethod
    @abc.abstractmethod
    def get_app_name(self):
        pass
    
    @abc.abstractmethod
    def run(self, landsmarks, frame):
        if not self.isOpen:
            return frame
        pass

    @abc.abstractmethod
    def open(self):
        pass
    
    @abc.abstractmethod
    def close(self):
        pass
    
    def __str__(self):
        return self.name + " - " + self.description