import unittest

from portal_src.bin.utils.lang import dict2obj, json2obj, obj2dict


class TestlangUtils(unittest.TestCase):

    def test_dict2obj(self):
        obs = dict2obj(dict(alist = [ 1,3,[3,4],dict(test='test', test2 = True)],test='bluvv', test1=False, test2= dict(bla='blubb')))
        self.assertEqual(obs.test, 'bluvv')
        self.assertFalse(obs.test1)
        self.assertEqual(obs.test2.bla, 'blubb')
        self.assertEqual(obs.alist[0], 1)
        self.assertEqual(obs.alist[2][1], 4)
        self.assertEqual(obs.alist[3].test, 'test')
        self.assertEqual(obs.alist[3].test2, True)


    def test_json2obj(self):
        obs = json2obj('{ "alist": [ 1,3,[3,4],{"test":"test", "test2" : true}] ,"test": "bluvv", "test1" : false, "test2" : { "bla":"blubb" } }')
        self.assertEqual(obs.test, 'bluvv')
        self.assertFalse(obs.test1)
        self.assertEqual(obs.test2.bla, 'blubb')
        self.assertEqual(obs.alist[0], 1)
        self.assertEqual(obs.alist[2][1], 4)
        self.assertEqual(obs.alist[3].test, 'test')
        self.assertEqual(obs.alist[3].test2, True)

    def test_obj2dict(self):
        obs = dict2obj(dict(alist = [ 1,3,[3,4],dict(test='test', test2 = True)],test='bluvv', test1=False, test2= dict(bla='blubb')))
        self.assertEqual(obs.test, 'bluvv')
        self.assertFalse(obs.test1)
        self.assertEqual(obs.test2.bla, 'blubb')
        self.assertEqual(obs.alist[0], 1)
        self.assertEqual(obs.alist[2][1], 4)
        self.assertEqual(obs.alist[3].test, 'test')
        self.assertEqual(obs.alist[3].test2, True)
        dic = obj2dict(obs, obs.__class__)
        self.assertEqual(dic['test'], 'bluvv')
        self.assertFalse(dic['test1'])
        self.assertEqual(dic['test2']['bla'], 'blubb')
        self.assertEqual(dic['alist'][0], 1)
        self.assertEqual(dic['alist'][2][1], 4)
        self.assertEqual(dic['alist'][3]['test'], 'test')
        self.assertEqual(dic['alist'][3]['test2'], True)