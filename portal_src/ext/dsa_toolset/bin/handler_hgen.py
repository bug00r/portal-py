import wx
from portal_src.bin.control import ControllerRequest

class HGHandlerFrameEvent(wx.PyEvent):
    def __init__(self, ident, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(ident)
        self.data = data


class HgenHandler(object):

    def __init__(self):
        self.__resmgr = None
        self.__UPDATE_HGEN_UI = wx.NewId()

    def hgen_init_ui(self, parameter):
        print("init res ui to init hgen")
        self.controller.submit(ControllerRequest(self.config.ident, "get_resmgr", parameter,
                                                 ControllerRequest(self.config.ident, "got_resmgr", None )))

    def got_resmgr(self, parameter):
        self.__resmgr = parameter.result
        print("ghen got resource mgr")

    def add_char(self, event):
        print("add new charackter")

    def rem_char(self, event):
        print("rem charackter")

"""
This Note is to update UI with XSLT whenn we need that

    def got_resmgr(self, parameter):
        self.__resmgr = parameter.result
        hgen_ui = self.__resmgr.get("hgen_main_ui")
        #hgen_template = self.__resmgr.get("hgen_main")
        prepareNS()
        #try:
            #xslt = etree.XSLT(hgen_template.doc())
            #xml_1 = etree.XSLT.strparam("<r1><y1 /><y1 /><y1 /></r1>")
            #xml_2 = etree.XSLT.strparam("<r2><x2 /><y2 /><y2 /></r2>")
            #result = xslt(hgen_ui.doc(), x1=xml_1, x2=xml_2)
            #transform to xrc
        res = xrc.XmlResource()
        #print(etree.tostring(result, pretty_print=True))
        #res.LoadFromBuffer(etree.tostring(result))
        res.LoadFromBuffer(etree.tostring(hgen_ui.doc()))
        self.ui.main.Connect(-1, -1, self.__UPDATE_HGEN_UI, self.update_hgen_ui_proc)
        wx.QueueEvent(self.ui.main, HGHandlerFrameEvent(self.__UPDATE_HGEN_UI, res))
        #except:
         #   for error in xslt.error_log:
        #        print(error.message, error.line)

    def update_hgen_ui_proc(self, parameter):

        hgen_panel = self.ui.main.FindWindow("hgen")
        #generated_hgen = self.ui.main.FindWindow("hgen_panel")
        generated_hgen = parameter.data.LoadPanel(parent=hgen_panel, name="hgen_panel")
        hgen_panel.GetSizer().Add(generated_hgen, flag=wx.EXPAND, proportion=1)
        hgen_panel.GetSizer().Layout()
        self.controller.submit(PortalBindEventRequest(self.config.ident, generated_hgen))

    def update_hgen_ui_proc_2(self, parameter):
        spell = self.ui.main.FindWindow("spell_panel")
        liturgie = self.ui.main.FindWindow("liturgie_panel")
        hgenbook = self.ui.main.FindWindow('hgen_notebook')
        hgenbook.RemovePage(hgenbook.FindPage(spell))
        hgenbook.RemovePage(hgenbook.FindPage(liturgie))



"""