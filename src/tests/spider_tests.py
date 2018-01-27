import unittest, time
from multiprocessing import Queue, Value

from ..jandan_spider import *
from src.tasks.get_tucao_task import *


logging.basicConfig(level=logging.DEBUG)


class SpiderTests(unittest.TestCase):

    def test_parse_url(self):
        ret = JandanSpider._parse_url("http://www.163.com")

        self.assertIsNotNone(ret)


if __name__ == "__main__":
    unittest.main()