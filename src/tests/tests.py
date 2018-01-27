import unittest, time
from multiprocessing import Queue, Value

from src.models import *
from src.tasks.get_tucao_task import *


logging.basicConfig(level=logging.DEBUG)


class UtilsTest(unittest.TestCase):

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


class PictureContainerTests(unittest.TestCase):

    def test_create(self):
        id = 123
        like = 456
        dislike = 0
        url = "fake"

        pic_c = PictureContainer(id, like, dislike, url)
        self.assertEqual(pic_c.id, id)
        self.assertEqual(pic_c.like, like)
        self.assertEqual(pic_c.dislike, dislike)
        self.assertEqual(pic_c.img_src, url)

    def test_to_str(self):
        id = 123
        like = 456
        dislike = 0
        url = "fake"

        pic_c = PictureContainer(id, like, dislike, url)
        self.assertEqual(pic_c.__str__(),
                         "Picture info:[id={}, img_src={}, like/dislike={}/{}]".format(id,
                                                                                       url,
                                                                                       like,
                                                                                       dislike))


class TucaoTaskTests(unittest.TestCase):

    def test_task(self):
        tucao_task_runner = GetPicTucaoTaskRunner()
        try:
            pic_id = "3673893"
            tucao_task_runner.start(pic_id)
            tucao_task_runner.start(pic_id)

            results = tucao_task_runner.get_results()
            self.assertEqual(len(results), 2)
            for ret in results:
                self.assertEqual(type(ret), list)
                for r in ret:
                    self.assertEqual(type(r), PictureTucao)
                    self.assertEqual(r.pic_id, pic_id)
        finally:
            tucao_task_runner.thread_pool.terminate()


if __name__ == "__main__":
    unittest.main()