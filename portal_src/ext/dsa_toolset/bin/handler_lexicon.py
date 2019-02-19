import wx
from mako.template import Template
from pathlib import Path
from wx import xrc
from portal_src.bin.control import ControllerRequest
from portal_src.ext._portal_.bin.request import PortalBindEventRequest

class LexiconHandlerFrameEvent(wx.PyEvent):
    def __init__(self, ident, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(ident)
        self.data = data

class LexiconHandler(object):

    def __init__(self):
        self.__resmgr = None
        self.__INIT_LEXICON_UI = wx.NewId()
        self.__keyword_ctrl = None
        self.__category = None
        self.__lex_search_result = None
        self.__lastdetail = None
        self.__groups = None

    def self_init_ui(self, parameter):
        self.__category = self.ui.main.FindWindow("categories")
        self.__groups = self.ui.main.FindWindow("groups")
        self.__keyword_ctrl = self.ui.main.FindWindow("search_keywords")
        self.__lex_search_result = self.ui.main.FindWindow("lex_search_result")
        self.ui.main.Connect(-1, -1, self.__INIT_LEXICON_UI, self.init_res_ui)
        self.controller.submit(ControllerRequest(self.config.ident, "get_resmgr", parameter, ControllerRequest(self.config.ident, "got_resmgr_lexicon", None )))

    def got_resmgr_lexicon(self, parameter):
        print("calls got_resmgr_lexicon")
        self.__resmgr = parameter.result
        wx.QueueEvent(self.ui.main, LexiconHandlerFrameEvent(self.__INIT_LEXICON_UI, None))

    def init_res_ui(self, parameter):
        print("init lexicon UI")
        self.__category.Append("All")
        self.__groups.Append("All")
        for res in self.__resmgr.names_and_types():
            if res[1] == ".xml":
                self.__category.Append(res[0])
                xml_entry = self.__resmgr.get(res[0])
                foundgroups = xml_entry.doc().xpath('//group')
                for group in foundgroups:
                    self.__groups.Append(group.get('name'))
        self.__category.SetSelection(0)
        self.__groups.SetSelection(0)

    def trigger_category_selected(self, parameter):
        selected_category = parameter.EventObject.GetValue()
        xml_entry = self.__resmgr.get(selected_category)
        foundgroups = xml_entry.doc().xpath('//group')
        self.__groups.Clear()
        self.__groups.Append("All")
        for group in foundgroups:
            self.__groups.Append(group.get('name'))
        self.__groups.SetSelection(0)

    def __search_and_display_result(self, doc, group, searchstring):
        if group == "All":
            search_path = "//group/*[re:match(@name,'{}')]".format(searchstring)
        else:
            search_path = "//group[@name = '{}']/*[re:match(@name,'{}')]".format(group, searchstring)
        result = doc.xpath(search_path, namespaces={"re": "http://exslt.org/regular-expressions"})
        for res_entry in result:
            newitm = self.__lex_search_result.Append(res_entry.get('name'))
            self.__lex_search_result.SetClientData(newitm, res_entry)

    def trigger_search(self, parameter):
        sel_cat = self.__category.GetStringSelection()
        keywords = self.__keyword_ctrl.GetValue()
        if len(keywords) > 0:
            if sel_cat != "All":
                search_nodes = [self.__resmgr.get(sel_cat)]
            else:
                search_nodes = [ self.__resmgr.get(res[0]) for res in self.__resmgr.names_and_types() if res[1] == ".xml" ]
            self.__lex_search_result.Clear()
            for entry in search_nodes:
                doc = entry.doc()
                selected_group = self.__groups.GetStringSelection()
                self.__search_and_display_result(doc, selected_group, keywords)

    def select_search_result(self, parameter):
        sel_idx = parameter.EventObject.GetSelection()
        sel_node = parameter.EventObject.GetClientData(sel_idx)

        node_template = getattr(self.config.lexicon.templates, sel_node.tag,
                                getattr(self.config.lexicon.templates,'default'))
        lex_detail_template = Path(__file__).parent.parent / "data" / "Templates" / node_template
        if lex_detail_template.exists():
            with lex_detail_template.open("r", encoding="utf-8") as file:
                template = file.read()
            if self.__lastdetail is not None:
                self.__lastdetail.Destroy()
            rendered_detail = Template(template).render(data=sel_node)
            res = xrc.XmlResource()
            res.LoadFromBuffer(bytes(rendered_detail,encoding="utf-8"))
            parent = self.ui.main.FindWindow("lex_detail_panel")
            self.__lastdetail = res.LoadPanel(parent=parent, name="lexicon_detail")
            parent.GetSizer().Add(self.__lastdetail, flag=wx.EXPAND, proportion=1)
            parent.GetSizer().Layout()
            self.controller.submit(PortalBindEventRequest(self.config.ident, self.__lastdetail, None))
        else:
            wx.MessageDialog(self.ui.main, "Lexicon Detail Template does not exist: " + lex_detail_template.__str__() ,
                             "Lexicon Detail Template not found...", wx.OK | wx.ICON_ERROR).ShowModal()

    def trigger_goto_group_result(self, event):
        sel_idx = self.__lex_search_result.GetSelection()
        if self.__lex_search_result.GetSelection() != wx.NOT_FOUND:
            sel_node = self.__lex_search_result.GetClientData(sel_idx)
            self.__lex_search_result.Clear()
            self.__search_and_display_result(sel_node.getparent().getparent(), sel_node.getparent().get('name'), ".")
