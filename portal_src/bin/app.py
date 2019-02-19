from portal_src.bin.utils.file import readconfigjson
from portal_src.bin.utils.lang import createinstance, getclass
import copy
from wx import xrc
import os
from pathlib import Path


class ExtensionCreator(object):
    def __init__(self, rootpath, dirname, controller, uimanager, extensionmgr):
        self.__root_path = rootpath
        self.__dirname = dirname
        self.__controller = controller
        self.__uimanager = uimanager
        self.__extmgr = extensionmgr

    def __createhandler(self, config):
        handlers = createinstance('HandlerList')

        ui = createinstance("Ui")
        for handlerentry in config.handler:
            print("create handler {0} {1}".format(handlerentry.modul, handlerentry.cls))
            try:
                handler = getclass(handlerentry.modul, handlerentry.cls)()
            except BaseException as e:
                print(e.args)
            print("class success")
            setattr(handler, 'path', self.__root_path)
            setattr(handler, 'dirname', self.__dirname)
            setattr(handler, 'config', config)
            setattr(handler, 'controller', self.__controller)
            setattr(handler, 'uipool', self.__uimanager)
            setattr(handler, 'ui',ui )
            #only for portalhandler get access to extensions
            if self.__dirname == "_portal_":
                setattr(handler, "extensions", self.__extmgr)
            setattr(handlers, handlerentry.name, handler)
        return handlers

    def create(self):
        curextpath = self.__root_path / self.__dirname
        print("extension path {0}".format(curextpath))
        config = readconfigjson(curextpath)
        print("extension path read config success")
        #1. Handler initialisieren
        handlers = self.__createhandler(config)
        print("Handler creation success")
        extension = createinstance('Extension')
        print("Extension instance success")
        setattr(extension, 'handler', handlers)
        setattr(extension, 'config', config)
        return extension


"""
    Hier muss ein XRC Manager hin.
    1. Er lädt extension bezogene XRC Dateien
    2. Er kann auch extensionübergreifende UI Elemente laden
    3. Er kann contextübergreifende Parentelemente definieren. Allerdings nur von vorher bereits geladenen
       Gui Elementen
    4. Jede Extension hat Zugriff auf den XRC Mgr. Das dient dazu sich anderer UI Elemente bedienen zu
       können.
    5. Geladenen UI Elemente können ein Ziel haben, wie z.B. Extension Hauptgui. Soll aber eine windowID
       (UI-Element) z.B. mehrfach verwendet werden hat sie keinen Prototyp und wird vom Handler gesetzt.

       Hat ein Panel oder Form oder was ein anderes Element ein Target. Wird es diesen zugewiesen. Diese
       Zuweisung erfolgt über eine Suche nach windowID vom Hauptfenster aus:

            search in Frame/Window windowID => wx.Window.FindWindow (self, id)
"""
class UiManager(object):
    def __init__(self, extensionrootpath):
        self.__root_path = extensionrootpath
        self.__cache = {}

    def __readxrc(self, config, curextpath):
        xrcpath = curextpath / Path(os.path.join(*config.ui.file))
        res = xrc.XmlResource()
        with xrcpath.open(mode='rb') as f:
            res.LoadFromBuffer(f.read())
        return res

    def __createxmlresource(self, extensionname):
        extpath = self.__root_path / extensionname
        config = readconfigjson(extpath)
        return self.__readxrc(config, extpath), config

    """
        "elements" : {
      "main" : { "cacheable": true, "type" : "Frame" , "params" : { "parent":null, "name":"Portal" } }

    def __getmainobject(self, xrcobj, config):
        func = getattr(xrcobj, "Load" + config.ui.mainelement.type)
        return func(**config.ui.mainelement.params.__dict__)
    },
    """
    def __createelement(self, uires, element, parent, elementconf):
        func = getattr(uires.xml, "Load" + elementconf.type)
        params = copy.deepcopy(elementconf.params)
        if parent is not None:
            params.parent = parent
        elif params.parent is not None:
            parentmeta = params.parent
            params.parent = self.get(params.parent.extension, params.parent.element)
            if hasattr(parentmeta,'sub') and parentmeta.sub is not None:
                params.parent = params.parent.FindWindow(parentmeta.sub)
        return func(**params.__dict__)

    def __getelement(self, uires, element, parent):
        if hasattr(uires.allocelements, element):
            reselement = getattr(uires.allocelements, element)
        else:
            elementconf = getattr(uires.config.ui.elements, element)
            reselement = self.__createelement(uires, element, parent, elementconf)
            if elementconf.cacheable:
                setattr(uires.allocelements, element, reselement)
        return reselement

    def get(self, extensionname, element, parent=None):
        if extensionname in self.__cache:
            print("ui from cache: {0}".format(extensionname))
            uiresource = self.__cache[extensionname]
        else:
            print("ui new: {0}".format(extensionname))
            xmlresource, config = self.__createxmlresource(extensionname)
            uiresource = createinstance("UiResource")
            setattr(uiresource, "xml", xmlresource)
            setattr(uiresource, "config", config)
            setattr(uiresource, "allocelements", createinstance("AllocElements"))

            self.__cache[extensionname] = uiresource

        element = self.__getelement(uiresource, element, parent)

        return element


class ExtensionManager(object):
    """
        1. read ext config(see above)
        2. load ui.file
        3. XmlResource.Load[ui.Portal[ui.mainelement]] // calls XmlResource.LoadFrame(TopEvelIfAny, ui.mainelement)
        4. cache loaded Frame
        5. Bind handler.
        5.1 Iterate over ui.handler
            - create and cache instances
        5.2 Iterate over ui.events
            - search in Frame/Window windowID => wx.Window.FindWindow (self, id)
            - iterate over events
                - bind each Found Event to given Handler from %.1 built handlercache
        6. attach new ui to portal center if there is no other target specified(null)
    """
    def __init__(self, extensionrootpath, controller, uimanager):
        #Path object
        self.__root_path = extensionrootpath
        self.__controller = controller
        self.__uimanager = uimanager
        self.__cache = {}

    def get(self, dirnameofext):
        if dirnameofext in self.__cache:
            print("extension from cache: {0}".format(dirnameofext))
            extension = self.__cache[dirnameofext]
        else:
            print("extension new: {0}".format(dirnameofext))
            extension = ExtensionCreator(self.__root_path, dirnameofext, self.__controller, self.__uimanager, self).create()
            print("extension new: {0} success".format(dirnameofext))
            self.__cache[dirnameofext] = extension
        return extension
