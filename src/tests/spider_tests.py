import unittest, time
from multiprocessing import Queue, Value

from src.models import *
from src.tasks.get_tucao_task import *


logging.basicConfig(level=logging.DEBUG)


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
        pic_id = "3673893"
        q = Queue()
        tucao_task_runner = GetPicTucaoTaskRunner(pic_id, q)

        tucao_task_runner.start()
        tucao_task_runner.join()

        self.assertTrue(not q.empty())
        tucao_li = q.get()
        self.assertTrue(len(tucao_li) > 0)
        self.assertTrue(isinstance(tucao_li[0], PictureTucao))


if __name__ == "__main__":
    unittest.main()