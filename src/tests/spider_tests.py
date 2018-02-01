import unittest, logging
from multiprocessing import Queue, Value, Lock

from src.models import *
from src.tasks.get_tucao_task import GetPicTucaoTaskRunner
from src.tasks.get_picture_task import GetPictureTaskRunner
from src.picture_filters import LikeDislikePictureFilter


logging.basicConfig(level=logging.INFO)


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


class TucaoModelTest(unittest.TestCase):

    def test_create(self):
        tucao = PictureTucao(12, 34, "\u3333", "\u4444\u9999", 10, 0)
        self.assertEqual(tucao.id, 12)
        self.assertEqual(tucao.pic_id, 34)
        self.assertEqual(tucao.author, "㌳")
        self.assertEqual(tucao.content, "䑄香")
        self.assertEqual(tucao.like, 10)
        self.assertEqual(tucao.dislike, 0)


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


class GetPictureTaskTests(unittest.TestCase):

    def test_task(self):
        queue = Queue()
        page_no = 180
        task = GetPictureTaskRunner(page_no, queue,
                                    LikeDislikePictureFilter(),
                                    200, Value('i', 0), Lock())
        task.start()
        task.join()

        self.assertTrue(not queue.empty())
        picture = queue.get()
        self.assertTrue(isinstance(picture, PictureContainer))
        self.assertTrue(picture.id is not None)
        self.assertTrue(len(picture.hot_tucao) > 0)

    def test_limited_task(self):
        queue = Queue()
        page_no = 200
        max_pic = 20
        counter = Value('i', 0)
        lock = Lock()

        tasks = []
        for _ in range(10):
            task = GetPictureTaskRunner(page_no, queue, LikeDislikePictureFilter(),
                                        max_pic, counter, lock)
            task.start()
            tasks.append(task)

        for t in tasks:
            t.join()

        count = 0
        while not queue.empty():
            queue.get()
            count += 1

        self.assertTrue(count == max_pic)


if __name__ == "__main__":
    unittest.main()
