import logging, time
from multiprocessing import Pool, Process
from src.jandan_spider import Spider
from urllib import request
import selenium.common.exceptions as sel_ex

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    while True:
        try:
            spider = Spider()
            spider.start()
        except BaseException as e:
            logger.error(e, exc_info=True)
            break

