"""
This module contains classes an function for managing nodes.
"""
import json
import hashlib

from ext.renderbug.bin.nodes.nodes_display import TextureDisplayNode
from ext.renderbug.bin.nodes.nodes_filter import AverageFilterNode, \
                                                      KernelFilterNode
from ext.renderbug.bin.nodes.nodes_noise import DiamondSquareNode, \
                                                     MidpointDisplacementNode
from ext.renderbug.bin.nodes.nodes_texture_synthesizer import JuliaSynthesizerNode, \
                                                                   MandelbrotSynthesizerNode, \
                                                                   NoiseSynthesizerNode


class NodeConfiguration(object):
    def get_config(self):
        """
        this function only get collection of Node Classes
        :return: List of Node Classes
        """
        return [TextureDisplayNode, AverageFilterNode, KernelFilterNode, DiamondSquareNode, MidpointDisplacementNode,
                JuliaSynthesizerNode, MandelbrotSynthesizerNode, NoiseSynthesizerNode]


class NodeEntry(object):

    def __init__(self, config, nodeclass, key):
        self.__config = config
        self.__nodeclass = nodeclass
        self.__key = key



class NodeManager(object):

    def __init__(self):
        self.__nodes = dict()
        self.__nodetree = dict()
        self.__init_nodes_()

    def __init_nodes_(self):
        """ Here we are preparing all nodes """
        for nodeclass in NodeConfiguration().get_config():
            jsonconfig = json.loads(nodeclass.__doc__)
            key_md5 = hashlib.md5()
            nodename = jsonconfig['name']
            key_md5.update(bytes("".join(nodename), encoding="utf-8"))
            key = key_md5.hexdigest()
            if key not in self.__nodes:
                self.__nodes[key] = NodeEntry(jsonconfig, nodeclass, key)

            basetree = self.__nodetree
            for cnt, namepart in enumerate(nodename, 1):
                if basetree.get(namepart, None) is None:
                    if cnt == len(nodename):
                        basetree[namepart] = key
                    else:
                        basetree[namepart] = dict()
                basetree = basetree[namepart]


    def get_nodes(self):
        """
         Thi function is searching all nodes. The result is structred like a simple tree based on dict.
         :return: dictionary with configured node names
        """
        return self.__nodetree

    def node(self, key):
        """

        :param key: md5 hashkey for identifying node tree value in nodes dict
        :return: found node or None
        """
        return self.__nodes.get(key, None)
