import wx
from portal_src.bin.utils.file import readconfigjson, json2obj
from portal_src.bin.control import ControllerRequest


class ShowPortalFrameEvent(wx.PyEvent):
    def __init__(self, ident, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(ident)
        self.data = data


class MenuInvoker(object):
    def __init__(self, request, controller):
        self.__request = request
        self.__controller = controller

    def invoke(self, event):
        self.__controller.submit(self.__request)


class PortalHandler():

    def __init__(self):
        self.__START_EVT_ID = wx.NewId()
        self.__INIT_EXT_MENU_EVT_ID = wx.NewId()
        self.__ADD_TO_MAIN_EVT_ID = wx.NewId()
        self.__BIND_EVT_ID = wx.NewId()

    def start(self, parameter):
        setattr(self.ui, 'main', self.uipool.get(self.dirname, 'main'))
        self.ui.main.Connect(-1, -1, self.__START_EVT_ID, self.showportalframe)
        wx.QueueEvent(self.ui.main, ShowPortalFrameEvent(self.__START_EVT_ID, None))

    def showportalframe(self, event):
        self.createandshowextmenu()
        self.ui.main.Show()
        self.ui.main.GetStatusBar().SetStatusText("Holy shit, that works!!!")

    def createandshowextmenu(self):
        extensionmenu = None
        for extension in self.path.iterdir():
            if extension.is_dir() and extension.name[0] != '_':
                extpath = self.path / extension.name
                extconfig = readconfigjson(extpath)
                menubar = self.ui.main.GetMenuBar()
                extensionmenuid = menubar.FindMenu("Extensions")
                if extensionmenuid == wx.NOT_FOUND:
                    extensionmenu = wx.Menu()
                    menubar.Append(extensionmenu, "Extensions")

                newitem = extensionmenu.Append(wx.NewId(), extconfig.name, extconfig.help)

                invoker = MenuInvoker(ControllerRequest(extension.name, "start"), self.controller)
                self.ui.main.Bind(wx.EVT_MENU, invoker.invoke, newitem)

    def addtomain(self, parameter):
        print('init extension menu')
        self.ui.main.Connect(-1, -1, self.__ADD_TO_MAIN_EVT_ID, self.addtomain_proc)
        wx.QueueEvent(self.ui.main, ShowPortalFrameEvent(self.__ADD_TO_MAIN_EVT_ID, parameter))

    def addtomain_proc(self, event):
        nb = self.ui.main.FindWindow("notebook")
        if nb.FindWindow(event.data.extension) is None:
            ext_obj = self.uipool.get(event.data.extension, event.data.uielement, nb)
            nb.AddPage(ext_obj, event.data.name, True)
            #todo event bindigs in own  handler every time based on method initui
            self.bind_events_proc(event.data.extension, ext_obj)
            self.controller.submit(ControllerRequest(event.data.extension, "initui", ext_obj))


    def bind_events(self, parameter):
        self.ui.main.Connect(-1, -1, self.__BIND_EVT_ID, self.bind_event_ui_proxy)
        wx.QueueEvent(self.ui.main, ShowPortalFrameEvent(self.__BIND_EVT_ID, parameter))


    def bind_event_ui_proxy(self, event):
        self.bind_events_proc(event.data.extension, event.data.ext_obj)


    def bind_events_proc(self, extension, ext_obj):
        extension = self.extensions.get(extension)
        for uielement in extension.config.ui.events:
            uiobj = ext_obj.FindWindow(uielement.name)
            if uiobj is not None:
                for uievent in uielement.event:
                    wxEvent = getattr(wx, uievent.name, None)
                    if wxEvent is not None:
                        for handler in uievent.handler:
                            handlerobj = getattr(extension.handler, handler.name, None)
                            if handlerobj is not None:
                                for func in handler.funcs:
                                    funcobj = getattr(handlerobj, func, self.invalid_event)
                                    ext_obj.Bind(wxEvent, funcobj, uiobj)
                            else:
                                print("handler not exist :(: {0}".format(handler.name))


    def invalid_event(self, event):
        print("invalid event")