import json
import Xponge

class Model():
    id = 0
    def __init__(self):
        self.id = Model.id
        Model.id += 1


class MACROS:
    VERSION = 0.1
    PACKAGE = "Visual Sponge"
    PORT = 10696
    DEBUG_MODE = False
    APP = None
    CMD = None
    TEXT = ""
    TEMP = None
    CHINESE_STRINGS = {
    "global.quitConfirmation": u"确定退出?",
    "global.ok": u"确定",
    "global.quit": u"退出",
    "global.cancel": u"取消",
    "global.saveFile": u"保存",
    "cocoa.menu.about": u"关于",
    "cocoa.menu.services": u"服务",
    "cocoa.menu.view": u"查看",
    "cocoa.menu.hide": u"隐藏",
    "cocoa.menu.hideOthers": u"隐藏其他",
    "cocoa.menu.showAll": u"全部显示",
    "cocoa.menu.quit": u"退出",
    "cocoa.menu.fullscreen": u"全屏 ",
    "windows.fileFilter.allFiles": u"所有文件",
    "windows.fileFilter.otherFiles": u"其他文件",
    "linux.openFile": u"打开文件",
    "linux.openFiles": u"打开文件",
    "linux.openFolder": u"打开文件夹",
    "file": u"文件",
    "display": u"显示",
    "settings": u"设置",
    "placeholder": u"占位",
    "help": u"帮助",
    "contact us": u"联系我们",
    "Welcome to Use Visual Sponge!": u"欢迎使用Visual Sponge！",
    " Version": u"版本",
    }
    ENGLISH_STRING = {}
    CURRENT_LANGUAGE = CHINESE_STRINGS
    @staticmethod
    def localization(key):
        return MACROS.CURRENT_LANGUAGE.get(key, key)
    class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Atom):
                return json.JSONEncoder.default(self, {key: o.__dict__[key] for key in o.__all__})
            if isinstance(o, Model):
                return json.JSONEncoder.default(self, o.atoms)
            return json.JSONEncoder.default(self, o)
