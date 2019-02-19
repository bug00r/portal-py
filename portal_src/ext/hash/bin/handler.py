from portal_src.ext._portal_.bin.request import PortalAddToMainRequest
import hashlib
import base64
import wx

class HashHandlerFrameEvent(wx.PyEvent):
    def __init__(self, ident, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(ident)
        self.data = data

class HashHandler(object):

    def __init__(self):
        self.__algorithm = {
            'b64encode': base64.b64encode,
            'b64decode': base64.b64decode,
            'b32encode': base64.b32encode,
            'b32decode': base64.b32decode,
            'b16encode': base64.b16encode,
            'b16decode': base64.b16decode,
            'a85encode': base64.a85encode,
            'a85decode': base64.a85decode
        }
        self.__INIT_ALGOS_EVT_ID = wx.NewId()

    def start(self, parameter):
        self.controller.submit(PortalAddToMainRequest(self.config.ident, "main", self.config.name))

    def initui(self, parameter):
        setattr(self.ui, "main", parameter)
        self.ui.main.Connect(-1, -1, self.__INIT_ALGOS_EVT_ID, self.initHashes)
        wx.QueueEvent(self.ui.main, HashHandlerFrameEvent(self.__INIT_ALGOS_EVT_ID, parameter))

    def initHashes(self, event):
        hashlist = self.ui.main.FindWindow('hashlist')
        hashlist.Append([algo for algo in self.__algorithm.keys()])
        hashlist.Append([algo for algo in hashlib.algorithms_available])

    def calchash(self, event):
        hashprocess = self.ui.main.FindWindow('hashlist').GetStringSelection()
        hashinput = self.ui.main.FindWindow('input').GetValue()
        if hashprocess != "":
            if hashprocess in self.__algorithm:
                process = getattr(base64, hashprocess, None)
                if process is not None:
                    result = process(bytes(hashinput, encoding='utf-8')).decode(encoding='ascii')
            else:
                process = hashlib.new(hashprocess)
                process.update(bytes(hashinput, encoding='utf-8'))
                result = process.hexdigest()
            self.ui.main.FindWindow('output').SetValue(result)
