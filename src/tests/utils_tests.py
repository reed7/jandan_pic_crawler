import unittest
import logging

from ..utils import *

logging.basicConfig(level=logging.DEBUG)


class UtilTests(unittest.TestCase):

    def test_parse_url(self):
        ret = parse_url_content_to_bs("http://www.163.com")

        self.assertIsNotNone(ret)

    def test_unicode_to_char_raise_e(self):
        unicode = "\\u9646"
        with self.assertRaises(TypeError):
            unicode_to_char(unicode)

        unicode = "\u23646"
        with self.assertRaises(TypeError):
            unicode_to_char(unicode)

        unicode = "abc"
        with self.assertRaises(TypeError):
            unicode_to_char(unicode)

    def test_unicode_to_char(self):
        unicode = "\u9646"
        ret = unicode_to_char(unicode)
        self.assertEqual("陆", ret)

    def test_unicode_to_char_empty(self):
        ret = unicode_to_char("")
        self.assertEqual("", ret)

        ret = unicode_to_char(None)
        self.assertEqual("", ret)

    def test_uni_to_str(self):
        ret = unicode_seq_to_str("\u9999\u9999")

        self.assertIsNotNone(ret)
        self.assertEqual(ret, '香香')


if __name__ == "__main__":
    unittest.main()
