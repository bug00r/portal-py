import json
from portal_src.bin.utils.lang import dict2obj, obj2dict
from pathlib import Path


class JsonDict(object):
    """
        converts raw string into json string. if string is invalid json the rawstring will discard and value
        ist set to None. Otherwise it contains Json dict
    """
    def __init__(self, rawstring):
        self.__valid = True
        self.__value = None
        if rawstring is not None:
            try:
                self.__value = json.loads(rawstring)
            except:
                self.__valid = False

    def value(self):
        return self.__value

    def valid(self):
        return self.__valid



class JsonConfigReader(object):

    def __init__(self, path, encoding="utf-8"):
        self.__path = path
        self.__json = None
        self.__enc = encoding

    """
        return s object of JasonDict
    """
    def read(self):
        if self.__json is None:
            try:
                with self.__path.open(encoding=self.__enc) as file:
                    self.__json = JsonDict(file.read())
            except:
                self.__json = None
        return self.__json


class JsonConfigWriter(object):

    def __init__(self, path, encoding="utf-8"):
        if path is not None and not isinstance(path, Path):
            raise RuntimeError("path should not be None and instance of pathlib.Path")
        self.__path = path
        self.__enc = encoding

    def write(self, jsondict):
        if jsondict is not None and jsondict.valid() and isinstance(jsondict, JsonDict):
            with self.__path.open("w", encoding=self.__enc) as file:
                file.write(json.dumps(jsondict.value()))

    def write_dict(self, regulardict):
        if regulardict is not None:
            td = obj2dict(regulardict, regulardict.__class__)
            config = json.dumps(td)
            with self.__path.open("w", encoding=self.__enc) as file:
                file.write(config)


class JsonConfigObject(object):

    def __init__(self, jsondict):
        self.__json = None
        self.__jsonobj = None
        if jsondict is not None and isinstance(jsondict, JsonDict):
            self.__json = jsondict
            self.__jsonobj = None

    def obj(self):
        if self.__jsonobj is None and self.__json is not None and self.__json.valid():
            self.__jsonobj = dict2obj(self.__json.value())
        return self.__jsonobj


class JsonConfig(object):

    def __init__(self, path):
        if path is not None and not isinstance(path, Path):
            raise RuntimeError("path should not be None and instance of pathlib.Path")
        self.__path = path
        self.__reader = JsonConfigReader(self.__path)
        self.__writer = JsonConfigWriter(self.__path)
        self.__obj = None

    def get(self):
        if self.__obj is None:
            jd = self.__reader.read()
            self.__obj = JsonConfigObject(jd).obj()
        return self.__obj

    def save(self):
        if self.__obj is not None:
            self.__writer.write_dict(self.__obj)
