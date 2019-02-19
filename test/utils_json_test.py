import unittest
from portal_src.bin.utils.json_.config import *
from pathlib import Path


class TestJsonUtils(unittest.TestCase):

    def test_json_dict(self):
        jd = JsonDict("""
        {
            "test": 24,
            "test2" : [1,2,"34", { "testin": 23 }],
            "bla" : {
                "blubb": "test"
            }
        }
        """)
        d = jd.value()
        self.assertEqual(d['test'], 24)
        self.assertEqual(d['bla']['blubb'], "test")

    def test_json_fail(self):
        jd = JsonDict("""
        {
            "test": 24,
            "test2" : [1,2,"34", { "testin": 23 }],
            "bla" : {
                "blubb": "test"

        """)
        self.assertIsNone(jd.value())
        self.assertFalse(jd.valid())

    def test_read_json(self):
        path = Path(__file__).parent / "test.json"
        reader = JsonConfigReader(path)
        result = reader.read()
        d = result.value()
        self.assertEqual(d['test'], 24)
        self.assertEqual(d['bla']['blubb'], "testäöüßß")

    def test_read_json_fail(self):
        path = Path(__file__).parent / "test1.json"
        reader = JsonConfigReader(path)
        result = reader.read()
        self.assertIsNone(result)

    def test_write_json(self):
        jd = JsonDict("""
        {
            "test": 24,
            "test2" : [1,2,"34", { "testin": 23 }],
            "bla" : {
                "blubb": "testäöüßß"
            }
        }
        """)
        path = Path(__file__).parent / "test2.json"
        writer = JsonConfigWriter(path)
        writer.write(jd)

    def test_write_json_fail(self):
        jd = JsonDict("""
        {
            "test": 24,
            "test2" : [1,2,"34", { "testin": 23 }],
            "bla" : {
                "blubb": "testäöüßß"

        """)
        path = Path(__file__).parent / "test3.json"
        writer = JsonConfigWriter(path)
        writer.write(jd)

    def test_json_obj(self):
        path = Path(__file__).parent / "test.json"
        reader = JsonConfigReader(path)
        result = reader.read()
        obj = JsonConfigObject(result).obj()
        self.assertTrue(hasattr(obj, "test"))
        self.assertEqual(obj.test, 24)

    def test_json_obj_fail(self):
        jd = JsonDict("""
        {
            "test": 24,
            "test2" : [1,2,"34", { "testin": 23 }],
            "bla" : {
                "blubb": "testäöüßß"

        """)
        obj = JsonConfigObject(jd).obj()
        if obj is not None:
            raise AssertionError("object should be none")

    def test_json_config(self):
        path = Path(__file__).parent / "config.json"
        config = JsonConfig(path)
        confobj = config.get()
        self.assertTrue(hasattr(confobj, "test"))
        self.assertEqual(confobj.test, 24)
        self.assertTrue(hasattr(confobj, "test2"))
        self.assertTrue(isinstance(confobj.test2, list))
        confobj.test2.append(1)
        config.save()

    def test_json_config_fail(self):
        path = Path(__file__).parent / "config2.json"
        config = JsonConfig(path)
        confobj = config.get()
        self.assertEqual(confobj, None)