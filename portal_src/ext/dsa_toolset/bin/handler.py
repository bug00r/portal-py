from portal_src.bin.control import ControllerRequest
from portal_src.ext._portal_.bin.request import PortalAddToMainRequest, PortalBindEventRequest
from portal_src.bin.utils.json_.config import JsonConfig
import wx
from pathlib import Path


class XmlEditHandlerFrameEvent(wx.PyEvent):
    def __init__(self, ident, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(ident)
        self.data = data


class XmlEditHandler(object):

    def __init__(self):
        self.__INIT_ALGOS_EVT_ID = wx.NewId()

    def start(self, parameter):
        self.controller.submit(PortalAddToMainRequest(self.config.ident, "main", self.config.name))

    def __init_or_create_config(self):
        path = Path(__file__).parent.parent.joinpath(*self.config.configs)
        if not path.exists():
            with path.open("w", encoding="utf-8") as file:
                file.write(self.config.configsdefault)
            raise RuntimeWarning("config file not exist create a new one")
        config = JsonConfig(path)
        confobj = config.get()
        setattr(self.config, 'main', confobj)
        setattr(self.config, 'ctrl', config)

    def initui(self, parameter):
        setattr(self.ui, "main", parameter)
        self.ui.main.Connect(-1, -1, self.__INIT_ALGOS_EVT_ID, self.initTools)
        wx.QueueEvent(self.ui.main, XmlEditHandlerFrameEvent(self.__INIT_ALGOS_EVT_ID, parameter))

    def initTools(self, event):
        self.__init_or_create_config()
        toollist = self.ui.main.FindWindow('toollist')
        for tool in self.config.tools:
            toollist.Append(tool.name)
        self.controller.submit(ControllerRequest(self.config.ident, "update_initresource", None))

    def selectTool(self, event):
        selectedTool = self.config.tools[event.GetSelection()]
        toolsbook = self.ui.main.FindWindow('tools_book')
        resmgr = self.uipool.get("dsa_toolset", selectedTool.ui, parent=toolsbook)
        page_index = toolsbook.FindPage(resmgr)
        if page_index == wx.NOT_FOUND:
            toolsbook.AddPage(resmgr, selectedTool.name)
            toolsbook.SetSelection(toolsbook.GetPageCount()-1)
            res_req = ControllerRequest(self.config.ident, selectedTool.start, resmgr)
            self.controller.submit(PortalBindEventRequest(self.config.ident, resmgr, res_req))
        elif page_index != toolsbook.GetSelection():
                toolsbook.SetSelection(page_index)
