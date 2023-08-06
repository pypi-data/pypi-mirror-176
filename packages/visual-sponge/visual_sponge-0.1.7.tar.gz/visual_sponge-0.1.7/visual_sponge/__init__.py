import json
import Xponge

class Model():
    id = 0
    def __init__(self):
        self.id = Model.id
        Model.id += 1


class MACROS:
    VERSION = "0.1.7"
    PACKAGE = "Visual Sponge"
    PORT = 10696
    DEBUG_MODE = False
    APP = None
    CMD = None
    TEXT = ""
    TEMP = None
    CHINESE_STRINGS = {
    "Really quit?": u"确定退出?",
    "file": u"文件",
    "display": u"显示",
    "settings": u"设置",
    "placeholder": u"占位",
    "help": u"帮助",
    "contact us": u"联系我们",
    "Welcome to Use Visual Sponge!": u"欢迎使用 Visual Sponge！",
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
