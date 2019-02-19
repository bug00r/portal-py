from portal_src.bin.utils.lang import json2obj


def readconfigjson(configpath, filename='config.json'):
    config = configpath / filename
    with config.open() as configfile:
        readconfig = json2obj(configfile.read())
    return readconfig