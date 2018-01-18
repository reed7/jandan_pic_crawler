import os

from bs4 import BeautifulSoup
from selenium import webdriver

from .models import PictureContainer
from .picture_filters import PictureFilter, LikeDislikePictureFilter
from .setup import *

logging.basicConfig(filename=LOG_FILE,
                    level=LOG_LEVEL,
                    format=LOG_FORMAT,
                    datefmt=LOG_DATE_FORMAT)

logger = logging.getLogger(__name__)


class Spider(object):

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
                self.max_pic_to_fetch = self.start_pic_id - self.stop_pic_id

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

        while self.max_pic_to_fetch > 0:
            logger.info("Starting the task from page %d", curr_pageno)
            page_soup = self._parse_url(JANDAN_PIC_URL_PAGENO.format(curr_pageno))

            pic_list = page_soup.find("ol", {"class": "commentlist"})
            pic_elements = pic_list.find_all("li")

            ret = []
            for pic_ele in pic_elements:
                pic_id = pic_ele['id']

                if pic_id == self.stop_pic_id: # Already reach the stop point
                    self.max_pic_to_fetch = 0
                    break

                if PICUTURE_ID_PREFIX not in pic_id:
                    continue

                pc = self._build_picture_container(pic_id, pic_ele, curr_pageno)
                if not pc:
                    continue

                self.max_pic_to_fetch -= 1
                ret.append(pc)

                if self.max_pic_to_fetch == 0:
                    logger.info("Max page limit reached, task finish!")
                    break

            if self.max_pic_to_fetch > 0:
                logger.info("Page %d finished!", curr_pageno)
                curr_pageno -= 1

        self._post_task()

        return ret

    def _get_start_pageno(self):
        """
        Calculate start page of the current task from the current first page number
        :return:
        """
        first_page = self._parse_url(JANDAN_PIC_URL)
        curr_page_str = self._curr_pageno(first_page)
        if curr_page_str.isdigit():
            return int(curr_page_str) - SEARCH_BACK
        else:
            raise ValueError("curr_page is not a number!!")

    def _curr_pageno(self, soup):
        return soup.find("span", {"class": "current-comment-page"}).string[1:-1]

    def _parse_url(self, url):
        driver = webdriver.PhantomJS()

        try:
            driver.get(url)
            ret = BeautifulSoup(driver.page_source, BEAUTIFUL_SOUP_BUILDER)
            return ret
        finally:
            driver.quit()

    def _get_start_pic_id(self, start_page_url):
        page_soup = self._parse_url(start_page_url)
        pic_id_str = page_soup.find("ol").li['id']
        return int(pic_id_str[pic_id_str.index('-')+1:])

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

    def _get_img_link(self, picture_div):
        div_ele = picture_div.div.div
        div_ele = div_ele.find_all("div")[1]
        if div_ele:
            return div_ele.p.a

    def _post_task(self):
        with open(LAST_TASK_STOP, "w+") as f:
            logger.info("Writing picture ID %d into file", self.start_pic_id)
            f.write(str(self.start_pic_id))


