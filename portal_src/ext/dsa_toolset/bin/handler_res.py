from portal_src.bin.utils.xml.resource import XmlFileResourceCacheEntry, XmlResourceManager
from portal_src.bin.control import ControllerRequest
from portal_src.ext._portal_.bin.request import PortalBindEventRequest
import wx
from pathlib import Path
from lxml import etree


class XmlResourceHandlerFrameEvent(wx.PyEvent):
    def __init__(self, ident, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(ident)
        self.data = data


class XmlResourceHandler(object):

    def __init__(self):
        self.__RES_DLG_SHOW_ID = wx.NewId()
        self.__RES_OK_ID = wx.NewId()
        self.__RES_CANCEL_ID = wx.NewId()
        self.__RES_REMOVE_ID = wx.NewId()
        self.__UPDATE_INIT_RES = wx.NewId()
        self.__RES_INIT_UI_ID = wx.NewId()
        self.__resmgr = XmlResourceManager()
        self.__root = None

    def update_initresource(self, parameter):
        self.ui.main.Connect(-1, -1, self.__UPDATE_INIT_RES, self.update_initresource_proc)
        wx.QueueEvent(self.ui.main, XmlResourceHandlerFrameEvent(self.__UPDATE_INIT_RES, None))

    def update_initresource_proc(self, parameter):
        if not hasattr(self.config.main, "resources"):
            setattr(self.config.main, "resources", self.config.main.__class__())
        else:
            self.__load_resources_config()

    def add_resource_ok(self, event):
        self.ui.main.Connect(-1, -1, self.__RES_OK_ID, self.add_resource_ok_proc)
        wx.QueueEvent(self.ui.main, XmlResourceHandlerFrameEvent(self.__RES_OK_ID, event.GetEventObject().GetTopLevelParent()))

    def add_resource_ok_proc(self, event):
        event.data.EndModal(wx.ID_OK)

    def add_resource_cancel(self, event):
        self.ui.main.Connect(-1, -1, self.__RES_CANCEL_ID, self.add_resource_cancel_proc)
        wx.QueueEvent(self.ui.main, XmlResourceHandlerFrameEvent(self.__RES_CANCEL_ID, event.GetEventObject().GetTopLevelParent()))

    def add_resource_cancel_proc(self, event):
        event.data.EndModal(wx.ID_CANCEL)

    def add_resource(self, event):
        resdlg = self.uipool.get(self.config.ident, "CreateResourceDlg", parent=self.ui.main)
        res_req = ControllerRequest(self.config.ident, "add_resource_show", resdlg)
        self.controller.submit(PortalBindEventRequest(self.config.ident, resdlg, res_req))

    def add_resource_show(self, parameter):
        self.ui.main.Connect(-1, -1, self.__RES_DLG_SHOW_ID, self.add_resource_show_proc)
        wx.QueueEvent(self.ui.main, XmlResourceHandlerFrameEvent(self.__RES_DLG_SHOW_ID, parameter))

    def __check_overwrite(self, res_name):
        overwrite_res = wx.ID_NO
        mustoverride = hasattr(self.config.main.resources, res_name)
        if mustoverride:
            overwrite_res = wx.MessageDialog(self.ui.main, "Resource Exist, wanna overwrite?", "Resource exist...",
                                             wx.YES_NO | wx.ICON_INFORMATION).ShowModal()
        shouldoverride = (overwrite_res == wx.ID_YES)
        return mustoverride, shouldoverride

    def __check_creation(self, fp, res_name, res_file):
        create = wx.ID_NO
        mustcreate = not fp.exists()
        if mustcreate:
            create = wx.MessageDialog(self.ui.main, "Resource File \"{0}\" not Exist! You want to create it?".format(res_file), "Resource file not exist...",
                                         wx.YES_NO | wx.ICON_INFORMATION).ShowModal()

        shouldcreate = (create == wx.ID_YES)
        if shouldcreate:
            with fp.open("w", encoding="utf-8") as newfile:
                newfile.write("")

        updatedconfig = not mustcreate or (mustcreate and shouldcreate)
        if updatedconfig:
            setattr(self.config.main.resources, res_name, res_file)
            self.config.ctrl.save()
        return updatedconfig

    def add_resource_show_proc(self, event):
        flag = event.data.ShowModal()
        if flag == wx.ID_OK:
            res_name = event.data.FindWindow("res_name").GetValue()
            res_file = event.data.FindWindow("res_file").GetPath()
            fp = Path(res_file)

            mustoverride, shouldoverride = self.__check_overwrite(res_name)

            if not mustoverride or (mustoverride and shouldoverride):
                updatedconfig = self.__check_creation(fp, res_name, res_file)
                if updatedconfig:
                    self.__load_resources_file_update_ui(res_name, res_file)

    def __load_add_res(self, subfolder, filetype):
        xslt_path = Path(__file__).parent.parent / "data" / subfolder
        for xslt_file in xslt_path.glob("*.{0}".format(filetype)):
            name = xslt_file.name.split(".")[0]
            self.__resmgr.add_resource(name, xslt_file.__str__())

    def __load_resources_config(self):
        for conf_res in self.config.resources:
            self.__load_add_res(conf_res[0], conf_res[1])
        for res_name, file_name in self.config.main.resources.__dict__.items():
            self.__resmgr.add_resource(res_name, file_name)

    def __load_resources_file_update_ui(self, res_name, file_name):
        resource = self.__resmgr.add_resource(res_name, file_name)
        self.__update_ui_with_resource(resource)

    def __update_ui_with_resource(self, resource):
        restree = self.ui.main.FindWindow("resource_tree")
        if self.__root is None:
            self.__root = restree.AddRoot("resources")
        newitem = restree.AppendItem(self.__root, resource.name())
        restree.SetItemData(newitem, resource)

        root = resource.doc().getroot()
        newitem = restree.AppendItem(newitem, root.tag)
        restree.SetItemData(newitem, root)
        if len(root.getchildren()) > 0:
            restree.SetItemHasChildren(newitem)

    def res_init_ui(self, parameter):
        self.ui.main.Connect(-1, -1, self.__RES_INIT_UI_ID, self.res_init_ui_proc)
        wx.QueueEvent(self.ui.main, XmlResourceHandlerFrameEvent(self.__RES_INIT_UI_ID, None))

    def res_init_ui_proc(self, parameter):
        for res_name in self.__resmgr.names():
            resource = self.__resmgr.get(res_name)
            self.__update_ui_with_resource(resource)

    def rem_resource(self, event):
        self.ui.main.Connect(-1, -1, self.__RES_REMOVE_ID, self.rem_resource_proc)
        wx.QueueEvent(self.ui.main, XmlResourceHandlerFrameEvent(self.__RES_REMOVE_ID, None))

    def rem_resource_proc(self, event):
        shouldremoveres = wx.MessageDialog(self.ui.main, "Do you want to remove resource?", "Resource file not exist...",
                                         wx.YES_NO | wx.ICON_INFORMATION).ShowModal()

        if shouldremoveres == wx.ID_YES:
            shouldremovefile = wx.MessageDialog(self.ui.main, "Do you want to remove resource file too?", "Resource file not exist...",
                                         wx.YES_NO | wx.ICON_INFORMATION).ShowModal()

            res_tree = self.ui.main.FindWindow("resource_tree")
            selected = res_tree.GetSelection()
            if self.__root == res_tree.GetItemParent(selected):
                res_name = res_tree.GetItemText(selected)
                removed = self.__resmgr.rem_resource(res_name)
                delattr(self.config.main.resources, res_name)
                self.config.ctrl.save()
                res_tree.Delete(selected)

                if removed is not None:
                    if shouldremovefile == wx.ID_YES:
                        try:
                            fp = Path(removed.filename())
                            fp.unlink()
                        except FileNotFoundError as e:
                            wx.MessageDialog(self.ui.main, e.strerror + " : " + removed.filename(), "File not found...",
                                             wx.OK | wx.ICON_ERROR).ShowModal()
                else:
                    wx.MessageDialog(self.ui.main, "Resource \"{0}\" not found !? :(.".format(res_name), "Resource not exist...",
                                             wx.OK | wx.ICON_INFORMATION).ShowModal()
            else:
                wx.MessageDialog(self.ui.main, "The selected item is not a resource.", "not a resource...",
                                             wx.OK | wx.ICON_INFORMATION).ShowModal()

    def want_to_expand(self, event):
        selected = event.GetItem()
        res_tree = self.ui.main.FindWindow("resource_tree")
        if res_tree.GetChildrenCount(selected, False) == 0:
            data = res_tree.GetItemData(selected)
            if isinstance(data, XmlFileResourceCacheEntry):
                children = data.doc().getroot()
            else:
                children = data

            for child in list(children):
                newitem = res_tree.AppendItem(selected, child.tag)
                res_tree.SetItemData(newitem, child)
                if len(child.getchildren()) > 0:
                    res_tree.SetItemHasChildren(newitem)

    def __add_element_node_text(self, data):
        if isinstance(data, XmlFileResourceCacheEntry):
            children = data.doc().getroot()
        else:
            children = data

        res_elem_text = self.ui.main.FindWindow("res_elem_text")
        res_elem_text.SetValue(etree.tostring(children, pretty_print=True))

    def want_to_display(self, event):
        selected = event.GetItem()
        res_tree = self.ui.main.FindWindow("resource_tree")
        data = res_tree.GetItemData(selected)
        self.__add_element_node_text(data)

    def get_resmgr(self, parameter):
        return self.__resmgr
