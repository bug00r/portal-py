from portal_src.bin.control import ControllerRequest
from portal_src.bin.utils.lang import json2obj


class PortalAddToMainRequest(ControllerRequest):
    def __init__(self, extensionname, uielement, configname, responserequest=None):
        requestparameter = json2obj(
                '{{"extension": "{0}" , "uielement": "{1}" , "name": "{2}" }}'.format(extensionname, uielement, configname)
        )
        super().__init__("_portal_", "addtomain", requestparameter, responserequest)


class PortalBindEventRequest(ControllerRequest):
    def __init__(self, extension, wxuiobject, responserequest=None):
        requestparameter = json2obj('{{"extension": "{0}" , "ext_obj": null}}'.format(extension))
        requestparameter.ext_obj = wxuiobject
        super().__init__("_portal_", "bind_events", requestparameter, responserequest)
