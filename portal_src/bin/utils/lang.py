import json
import importlib
import inspect


def getclass(module, classname):
        module = importlib.import_module(module)
        print("import module done")
        clazz = inspect.getmembers(module, lambda obj: inspect.isclass(obj) and obj.__name__ == classname)
        print("cless member done")
        return clazz[0][1]


def __objfromvalue(value, clazz):
    result = value
    if isinstance(value, list):
        result = []
        for element in value:
            result.append(__objfromvalue(element, clazz))
    elif isinstance(value, dict):
        result = dict2obj(value, clazz=clazz)
    return result


def createinstance(classname, baseclasses=[], basedict=dict()):
    return type(classname, tuple(baseclasses), basedict)()


def createclass(classname, baseclasses=[], basedict=dict()):
    return type(classname, tuple(baseclasses), basedict)


def dict2obj(dictionary, classname='DictObj', clazz=None):
    if clazz is None:
        clazz = createclass(classname)
    dictobj = clazz()

    for key, value in dictionary.items():
        setattr(dictobj, key, __objfromvalue(value, clazz))

    return dictobj


def __objfromvalue_reverse(value, clazz):
    result = value
    if isinstance(value, list):
        result = []
        for element in value:
            result.append(__objfromvalue_reverse(element, clazz))
    elif isinstance(value, clazz):
        result = obj2dict(value, clazz)
    return result


def obj2dict(dictionary, clazz):
    newdict = {}

    for key, value in dictionary.__dict__.items():
        newdict[key] = __objfromvalue_reverse(value, clazz)

    return newdict


def json2obj(jsonstring):
    return dict2obj(json.loads(jsonstring))