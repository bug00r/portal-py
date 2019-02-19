from pathlib import Path
from lxml import etree
from io import StringIO, BytesIO
import sys


class XmlResource(object):

    def __init__(self, path, name, suffix='.xml'):
        if not isinstance(path, Path):
            raise RuntimeError("path must be type of \"pathlib.Path\"")
        if not isinstance(name, str):
            raise RuntimeError("name must be type of \"str\"")
        self.__path = path
        self.__name = name
        self.__xml = None
        self.__suffix = suffix

    def load(self):
        filename = self.__name + self.__suffix
        for file in self.__path.glob(filename):
            with open(file.__str__(), encoding="utf-8") as _file:
                self.__xml = _file.read()

    def xml(self):
        if self.__xml is None:
            self.load()
        return self.__xml

    def suffix(self):
        return self.__suffix

    def name(self):
        return self.__name


class XmlDocument(object):

    def __init__(self, xml):
        if xml is None:
            self.__xml = "<error>Xml File should not be None</error>"
        else:
            self.__xml = xml
        self.__doc = None

    def __parse_xml(self):
        try:
            #f = StringIO(self.__xml)
            #self.__doc = etree.parse(f)
            fb = BytesIO(self.__xml.encode())
            self.__doc = etree.parse(fb)
        except:
            self.__xml = "".join(["<error>", "{0}".format(sys.exc_info()[1]), "</error>"])
            self.__parse_xml()

    def doc(self):
        if self.__doc is None:
            self.__parse_xml()
        return self.__doc

    def error(self):
        return self.__error


class XmlFileResourceCacheEntry(object):
    def __init__(self, name, resource, document, file_name):
        self.__name = name
        self.__resource = resource
        self.__document = document
        self.__filename = file_name

    def doc(self):
        return self.__document.doc()

    def xml(self):
        return self.__resource.xml()

    def filename(self):
        return self.__filename

    def name(self):
        return self.__name

    def suffix(self):
        return self.__resource.suffix()


class XmlResourceManager(object):

    def __init__(self):
        self.__cache = {}

    def add_resource(self, res_name, file_name):
        fp = Path(file_name)
        resource = XmlResource(fp.parent, fp.name.split('.')[0], fp.suffix)
        document = XmlDocument(resource.xml())
        cacheEntry = XmlFileResourceCacheEntry(res_name, resource, document, file_name)
        self.__cache[res_name] = cacheEntry
        return cacheEntry

    def rem_resource(self, res_name):
        removed = self.__cache.get(res_name)
        if removed is not None:
            del self.__cache[res_name]
        return removed

    def get(self, name):
        return self.__cache.get(name)

    def names(self):
        return self.__cache.keys()

    def names_and_types(self):
        return [( item.name(), item.suffix() ) for name, item in self.__cache.items()]
