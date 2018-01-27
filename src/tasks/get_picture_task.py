from multiprocessing import Process, Queue
import time

from src.setup import *
from src.utils import parse_url_content_to_bs
from src.models import PictureContainer
from .get_tucao_task import GetPicTucaoTaskRunner

logger = logging.getLogger(__name__)


class GetPictureTaskRunner(Process):

    def __init__(self, page_no, queue, pic_filter):
        Process.__init__(self)
        self.queue = queue
        self.page_no = page_no
        self.picture_filter = pic_filter

    def run(self):

        logger.info("Starting the task from page %d", self.page_no)

        page_soup = parse_url_content_to_bs(JANDAN_PIC_URL_PAGENO.format(self.page_no))
        pic_list = page_soup.find("ol", {"class": "commentlist"})

        # jandan may return a JSON string stating 'too many requests',
        # in this case, pic_list will be None
        sleep_sec = 2
        while not pic_list and sleep_sec <= sleep_sec * 2 * 2 * 2:
            logger.warning("Can't find picture list, waiting {} seconds to retry..".format(sleep_sec))
            time.sleep(sleep_sec)
            page_soup = parse_url_content_to_bs(JANDAN_PIC_URL_PAGENO.format(self.page_no))
            pic_list = page_soup.find("ol", {"class": "commentlist"})
            sleep_sec *= 2

        if sleep_sec > sleep_sec * 2 * 2 * 2 and not pic_list:
            logger.error("Failed to get page content, mission aborted!")
            return

        pic_elements = pic_list.find_all("li")
        tucao_tasks = []
        pic_results = {}
        tucao_queue = Queue()

        for pic_ele in pic_elements:
            pic_id = pic_ele['id']

            if PICUTURE_ID_PREFIX not in pic_id:
                logger.info("{} is not a picture ID! Skipped!".format(pic_id))
                continue

            pic_id = pic_id[len(PICUTURE_ID_PREFIX):]
            pc = self._build_picture_container(pic_id, pic_ele, self.page_no)
            if not pc:
                continue

            tucao_task_runner = GetPicTucaoTaskRunner(pic_id, tucao_queue)
            tucao_task_runner.start()
            tucao_tasks.append(tucao_task_runner)

            pic_results[pic_id] = pc

        # Wait for tucao tasks to complete
        for tucao_t in tucao_tasks:
            tucao_t.join()

        while not tucao_queue.empty():
            tucao_li = tucao_queue.get(block=False)
            if tucao_li:
                curr_pic_id = tucao_li[0].pic_id
                pic_results[curr_pic_id].hot_tucao = tucao_li

        for pic in pic_results.values():
            self.queue.put(pic)

        # TODO how to terminate the task when the end condition was met ?

    def _build_picture_container(self, pic_id, pic_ele, curr_pageno):
        logger.info("Parsing picture {}".format(pic_id))

        # fetch number of likes and dislikes
        vote_div = pic_ele.div.find("div", {"class": "jandan-vote"})
        like_span = vote_div.find("span", {"class": "tucao-like-container"})
        unlike_span = vote_div.find("span", {"class": "tucao-unlike-container"})
        like = int(like_span.span.string)
        dislike = int(unlike_span.span.string)

        pc = PictureContainer(pic_id, like, dislike)

        if self.picture_filter.accept(pc):
            img_src = self._get_img_link(pic_ele)

            if img_src:
                pc.img_src = img_src["href"]
                logger.debug(pc)
                return pc  # Only picture with a link is valid
            else:
                logger.warning("Can't find link for image %s at page %d!", pic_id, curr_pageno)

    @classmethod
    def _get_img_link(cls, picture_div):
        div_ele = picture_div.div.div
        div_ele = div_ele.find_all("div")[1]
        if div_ele:
            return div_ele.p.a

