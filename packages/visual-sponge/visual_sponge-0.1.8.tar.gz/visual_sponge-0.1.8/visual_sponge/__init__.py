import Xponge


class Model():
    id = 0
    models = {}
    WORKING = None
    def __init__(self, name, atoms, crds=None):
        self.name = name
        self.id = Model.id
        self.atoms = atoms
        self.crds = crds
        Model.models[self.id] = self
        Model.id += 1

    def __repr__(self):
        return f"Model(name={self.name}, id={self.id})"

    def __str__(self):
        return repr(self)


class MACROS:
    VERSION = "0.1.8"
    PACKAGE = "Visual Sponge"
    PORT = 10696
    DEBUG_MODE = False
    APP = None
    CMD = None
    TEXT = ""
    TEMP = None
    TAB = "\t"
    CHINESE_STRINGS = {
    "Show": u"显示",
    "Model": u"模型",
    "Atom": u"原子",
    "Frame": u"帧",
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
