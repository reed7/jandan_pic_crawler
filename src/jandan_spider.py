import os
import multiprocessing as mp

from .picture_filters import PictureFilter, LikeDislikePictureFilter
from .tasks.get_picture_task import GetPictureTaskRunner
from .setup import *
from .utils import parse_url_content_to_bs, MyJSONEncoder

logging.basicConfig(filename=LOG_FILE,
                    level=LOG_LEVEL,
                    format=LOG_FORMAT,
                    datefmt=LOG_DATE_FORMAT)

logger = logging.getLogger(__name__)


class JandanSpider(object):

    def __init__(self):
        self.start_pageno = -1
        self.start_pic_id = -1
        self.stop_pic_id = -1
        self.max_pic_to_fetch = DEFAULT_PIC_PER_TASK
        self.picture_filter = LikeDislikePictureFilter()
        self.initialized = False

    def init(self):
        if self.initialized:
            return True

        logger.info("Initializing the task...")

        # grab start page no
        self.start_pageno = self._get_start_pageno()

        # set limit for this task as end condition
        if os.path.isfile(LAST_TASK_STOP):
            with open(LAST_TASK_STOP) as f:
                line = f.readline()
                if line.isdigit():
                    self.stop_pic_id = int(line)

        start_page_url = JANDAN_PIC_URL_PAGENO.format(self.start_pageno)

        self.start_pic_id = self._get_start_pic_id(start_page_url)
        if self.stop_pic_id == self.start_pic_id:
            logger.info("No new pictures!")
            return False
        else:
            if self.stop_pic_id != -1:
                self.max_pic_to_fetch = \
                    min(self.max_pic_to_fetch, self.start_pic_id - self.stop_pic_id)

        logger.info("Picture limit set to %d", self.max_pic_to_fetch)
        self.initialized = True
        return True

    def set_picture_filter(self, pic_filter):
        if type(pic_filter) is not PictureFilter:
            raise ValueError("Type of pic_filter must be picture_filters.PictureFilter!!")

        self.picture_filter = pic_filter

    def start(self):

        if not self.initialized:
            logger.info("Initializing task hasn't been run, starting now...")
            if not self.init():
                return

        curr_pageno = self.start_pageno
        ret = []
        queue = mp.Queue()
        pic_got = 0

        while True:
            task_li = []
            for i in range(TASK_BATCH_SIZE):
                pic_task = GetPictureTaskRunner(curr_pageno, queue, self.picture_filter)
                pic_task.start()
                task_li.append(pic_task)
                curr_pageno -= 1

            for t in task_li:
                t.join()

            while not queue.empty():
                ret.append(queue.get(block=False))
                pic_got += 1

            # The problem of stop the task on the main process is,
            # the number of pictures fetched may reach the limit in the
            # middle of any get picture task
            if pic_got >= self.max_pic_to_fetch:
                logger.info("Got {} pictures, task finished!".format(pic_got))
                break

        self._post_task()

        # return ret
        json_encoder = MyJSONEncoder()
        with open("result_json", "w+") as ret_file:
            for r in ret:
                ret_file.write(json_encoder.encode(r))

    def _get_start_pageno(self):
        """
        Calculate start page of the current task from the current first page number
        :return:
        """
        first_page = parse_url_content_to_bs(JANDAN_PIC_URL)
        curr_page_str = self._curr_pageno(first_page)
        if curr_page_str.isdigit():
            return int(curr_page_str) - SEARCH_BACK
        else:
            raise ValueError("curr_page is not a number!!")

    @classmethod
    def _curr_pageno(cls, soup):
        return soup.find("span", {"class": "current-comment-page"}).string[1:-1]

    @classmethod
    def _get_start_pic_id(cls, start_page_url):
        page_soup = parse_url_content_to_bs(start_page_url)
        pic_id_str = page_soup.find("ol").li['id']
        return int(pic_id_str[pic_id_str.index('-')+1:])

    def _post_task(self):
        with open(LAST_TASK_STOP, "w+") as f:
            logger.info("Writing picture ID %d into file", self.start_pic_id)
            f.write(str(self.start_pic_id))

