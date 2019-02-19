from portal_src.bin.control import ControllerRequest
from portal_src.ext.renderbug.bin.nodes.nodes import NodeManager

import wx
from portal_src.bin.math.algorithm.noise import MidpointDisplacement
from portal_src.bin.math.utils import interpolate_lin
import array

class RenderHandlerFrameEvent(wx.PyEvent):
    def __init__(self, ident, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(ident)
        self.data = data


class View(wx.Panel):
    def __init__(self, parent):
        super(View, self).__init__(parent, size=wx.Size(513, 513))
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.__bitmap = wx.Bitmap(wx.Size(513, 513))

    def setimagebuffer(self, buffer):
        self.__bitmap = wx.Bitmap.FromBuffer(513, 513, buffer)

    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.__bitmap, 0, 0)


class RenderHandler(object):

    def __init__(self):
        self.__canvas = None
        self.__INIT_NOISE_EVT_ID = wx.NewId()
        self.__SHOW_NOISE_EVT_ID = wx.NewId()
        self.__nodemgr = NodeManager()

    def __init_canvas(self):
        print("init canvas")
        viewpanel = self.ui.main.FindWindow('viewpanel')
        self.__canvas = View(viewpanel)
        viewpanel.GetSizer().Add(self.__canvas, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
        viewpanel.Refresh()
        viewpanel.Update()

    def generatenoise(self, parameter):
        print("pgenerate_noise")
        if self.__canvas is None:
            self.__init_canvas()
        self.controller.submit(ControllerRequest("renderbug", "createnoise", None))

    def createnoise(self, parameter):
        print("create noise")
        self.ui.main.Connect(-1, -1, self.__SHOW_NOISE_EVT_ID, self.create_noise)
        wx.QueueEvent(self.ui.main, RenderHandlerFrameEvent(self.__SHOW_NOISE_EVT_ID, None))

    def create_noise(self, parameter):
        self.ui.main.FindWindow('generatenoise').Disable()
        size = 513
        md = MidpointDisplacement(size, size)
        md.create()
        noise = md.noise()
        min_ = noise.min()
        max_ = noise.max()
        buffsize = 513**2 * 3
        buffer =  array.array('B',(0,)*buffsize)
        for cnt, x in enumerate(noise.map()):
            val = int(interpolate_lin(x, min_, 0.0, max_, 255.0))
            base = cnt*3
            buffer[base] = val
            buffer[base + 1] = val
            buffer[base + 2] = val

        self.__canvas.setimagebuffer(buffer)
        self.__canvas.Refresh()
        self.ui.main.FindWindow('generatenoise').Enable()
