from queue import Queue
from portal_src.bin.app import ExtensionManager, UiManager
from portal_src.bin.utils.lang import json2obj
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import time

'''
    The Controller Request specified Requests which can handle by the controller itself.
    Parameter:
        - extension:    The identifier of target extension(Here we found the public interfaces)
        - pub_interface:The name of the public interface we want to call with our parameter
        - parameter:    The parameter for the public interface call
        - response:     The Response must be an Object of Type Controller Request. If the Request
                        containing results this results will forward to this request.
'''


class ControllerRequest(object):
    def __init__(self, extension, pub_interface, parameter=None, response=None):
        if extension is None or pub_interface is None:
            raise BaseException("We need extension and interface for request call")
        if response is not None and not isinstance(response, ControllerRequest):
            raise BaseException("response must be from Type Controller Request")
        self.extension = extension
        self.interface = pub_interface
        self.parameter = {"parameter": parameter}
        self.response = response

    def set_result(self, result):
        if self.parameter["parameter"] is None:
            self.parameter["parameter"] = json2obj("{}")
        setattr(self.parameter["parameter"], "result", result)


class MainController(object):
    def __init__(self, appobj, apppath, appconfig):
        self.__app = appobj
        self.__appruns = True
        self.__apppath = apppath
        self.__appconfig = appconfig
        self.__reqqueue = Queue()
        self.__resqueue = Queue()
        self.__reqexecuter = ThreadPoolExecutor(max_workers=5)
        self.__resexecuter = ThreadPoolExecutor(max_workers=5)
        self.__ctrlreqthread = Thread(target=self.__check_req_processing)
        self.__ctrlreqthread.start()
        self.__ctrlresthread = Thread(target=self.__check_res_processing)
        self.__ctrlresthread.start()
        completeextension = self.__apppath / appconfig.extensionpath
        self.__uimanager = UiManager(completeextension)
        self.__extensions = ExtensionManager(completeextension, self, self.__uimanager)


    def stop(self):
        self.__reqexecuter.shutdown(1)
        self.__resexecuter.shutdown(1)
        self.__appruns = False

    def initMain(self, request):
        return self.__process_request(request)


    def __check_req_processing(self):
        while self.__appruns:
            if not self.__reqqueue.empty():
                self.__resqueue.put(self.__reqexecuter.submit(self.__process_request, self.__reqqueue.get()))
            else:
                time.sleep(0.005) # yielding

    """
    "public": {
    "start" : [
      { "name" : "PortalHandler", "funcs" : ["start"] }
    ]
  },
    """
    def __process_request(self, request):
        if not isinstance(request, ControllerRequest):
            raise BaseException("request must be from Type Controller Request")
        extension = self.__extensions.get(request.extension)
        handlerconfigs = getattr(extension.config.public, request.interface)
        result = []
        for hndlconf in handlerconfigs:
            handler = getattr(extension.handler, hndlconf.name)
            for func in hndlconf.funcs:
                interface = getattr(handler, func)
                if request.parameter is not None:
                    result.append(interface(**request.parameter))
                else:
                    result.append(interface())
        lenres = len(result)
        if lenres == 1:
            result = result[0]
        elif lenres == 0:
            result = None
        return result, request.response

    def __check_res_processing(self):
        while self.__appruns:
            if not self.__resqueue.empty():
                res_future = self.__resqueue.get()
                if res_future.done():
                    self.__resexecuter.submit(self.__process_response, res_future)
                else:
                    self.__resqueue.put(res_future)
                    time.sleep(0.005)
            else:
                time.sleep(0.005) # yielding

    def __process_response(self, future):
        try:
            result, response = future.result()
            exception = future.exception()
            if exception is not None:
                raise exception
            if response is not None:
                if result is not None:
                    response.set_result(result)
                self.submit(response)
        except Exception as exc:
            print('generated an exception: {0}'.format(exc.__traceback__()))
        else:
            print('generated result: {0}'.format(result))


    def submit(self, request):
        self.__reqqueue.put(request)
