import wx
from portal_src.bin.control import MainController, ControllerRequest
import os
from portal_src.bin.utils.file import readconfigjson
from pathlib import Path

class PortalApp(wx.App):
    def __init__(self):
        self.__apppath = Path(os.path.join(os.path.dirname(os.path.realpath(__file__)), "portal_src")).resolve()
        self.__appconfig = readconfigjson(self.__apppath)
        self.__controller = MainController(self, self.__apppath, self.__appconfig)
        super().__init__()

    def OnInit(self):
        appinitsuccess = True
        self.__controller.initMain(ControllerRequest(self.__appconfig.startrequest.extension,
                                         self.__appconfig.startrequest.interface))
        return appinitsuccess

    def OnExit(self):
        self.__controller.stop()
        return 0


def main():
    app = PortalApp()
    app.MainLoop()


if __name__ == '__main__':
    main()