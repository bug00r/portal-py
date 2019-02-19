import types, sys, builtins


class Assembler(object):

    def __init__(self, descriptor):
        self.__descriptor = descriptor

    def get_attribute(self, _module, _typename):
        curmodule = _module
        for part in _typename.split("."):
            if hasattr(curmodule, part):
                curmodule = getattr(curmodule, part)
            else:
                break
        return curmodule

    def create_type(self,_module, _type):
        baselist = []
        if hasattr(_type, 'base') and isinstance(_type.base, list):
            for _typename in _type.base:
                if hasattr(builtins, _typename):
                    baselist.append(getattr(builtins, _typename))
                else:
                    clz = self.get_attribute(_module, _typename)
                    if clz is not None:
                        baselist.append(clz)
        clazz = type(_type.name, tuple(baselist), dict())
        return clazz

    def create_module(self, parentmodul, _module):
        module = types.ModuleType(_module.name)
        if hasattr(_module, 'types'):
            for _type in _module.types:
                setattr(module, _type.name, self.create_type(parentmodul, _type))
        if hasattr(_module, 'modules'):
            for submodule in _module.modules:
                setattr(module, submodule.name, self.create_module(module, submodule))
        return module

    def create(self):
        sys.modules[self.__descriptor.name] = self.create_module(None, self.__descriptor);


if __name__ == '__main__':
    from portal_src.bin.utils.lang import json2obj
    test_config = """
        {
            "name": "dsa41",
            "types": [
                { "name": "Text", "base": ["str"] },
                { "name": "Float", "base": ["float"] },
                { "name": "Integer", "base": ["int"] }
            ],
            "modules": [
                {
                  "name": "extend",
                  "types": [
                    { "name": "NextFloat", "base": ["Float"]  }
                  ]
                }
            ]
        }
        """
    descriptor = json2obj(test_config)
    assembler = Assembler(descriptor)
    assembler.create()
    import dsa41
    print(dsa41.Text("argh"))
    print(dsa41.Integer(10))
    print(dsa41.Float(10e-3))
    print(dsa41.extend.NextFloat(34.666666))

