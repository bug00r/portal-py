from portal_src.ext._portal_.bin.request import PortalAddToMainRequest, PortalBindEventRequest
from portal_src.ext.renderbug.bin.nodes.nodes import NodeManager

import wx


class RenderHandlerFrameEvent(wx.PyEvent):
    def __init__(self, ident, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(ident)
        self.data = data


class RenderHandler(object):

    def __init__(self):
        self.__INIT_NOISE_EVT_ID = wx.NewId()
        self.__nodemgr = NodeManager()
        self.__features_root = None
        self.__renderer_features = None
        self.__rendertreenb = None

    def start(self, parameter):
        self.controller.submit(PortalAddToMainRequest(self.config.ident, "main", self.config.name))

    def initui(self, parameter):
        setattr(self.ui, "main", parameter)
        self.ui.main.Connect(-1, -1, self.__INIT_NOISE_EVT_ID, self.initData)
        wx.QueueEvent(self.ui.main, RenderHandlerFrameEvent(self.__INIT_NOISE_EVT_ID, None))

    def __init_feature_item(self, tree, parentnode, featuredict):
        for feature in featuredict.keys():
            newnode = tree.AppendItem(parentnode, feature)
            fval = featuredict.get(feature, None)
            if fval is not None:
                if isinstance(fval, dict):
                    self.__init_feature_item(tree, newnode, fval)
                elif isinstance(fval, str):
                    tree.SetItemData(newnode, fval)


    def initData(self, parameter):
        features = self.__nodemgr.get_nodes()
        if self.__renderer_features is None:
            self.__renderer_features = self.ui.main.FindWindow('renderer_features')
        if self.__features_root is None:
            self.__features_root = self.__renderer_features.AddRoot("features")
        self.__init_feature_item(self.__renderer_features, self.__features_root,features)
        if self.__rendertreenb is None:
            self.__rendertreenb = self.ui.main.FindWindow('render_tree_nb')

    def add_new_feature(self, parameter):
        selected_node = parameter.GetItem()
        key = self.__renderer_features.GetItemData(selected_node)
        if key is not None:
            selection = self.__rendertreenb.GetSelection()
            if selection != wx.NOT_FOUND:
                self.__add_feature_to_current_rendertree(key, selection)
            else:
                wx.MessageDialog(self.ui.main, "No Render tree for adding \'{0}\' feature.".format(key),
                                               "No Render Tree available",
                                                wx.OK | wx.ICON_ERROR).ShowModal()

    def __add_feature_to_current_rendertree(self, key, selection):
        cur_rendertree = self.__rendertreenb.GetPage(selection)
        tree = cur_rendertree.FindWindow("render_tree_ctrl")
        if tree is not None:
            cur_item = tree.GetFocusedItem()
            new_item = tree.AppendItem(cur_item, key)
            instanceoffeature = None
            tree.SetItemData(new_item, instanceoffeature)

    def add_render_tree(self, parameter):
        rendertree = self.uipool.get(self.dirname, 'render_tree', self.__rendertreenb)
        self.__rendertreenb.AddPage(rendertree, "RT - {0}".format(self.__rendertreenb.GetPageCount()), True)
        tree = rendertree.FindWindow("render_tree_ctrl")
        root = tree.AddRoot("Render-Chain")
        tree.SelectItem(root)
        self.controller.submit(PortalBindEventRequest(self.config.ident, rendertree))

    def del_render_tree(self, parameter):
        selection = self.__rendertreenb.GetSelection()
        if selection != wx.NOT_FOUND:
            page = self.__rendertreenb.GetPage(selection)
            self.__rendertreenb.RemovePage(selection)
            page.Destroy() #this is because every rendertree page entry is a prototype and not a singleton