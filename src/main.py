#!/usr/bin/env python

import logging

import src.jandan_spider as js
import src.setup as setup


logging.basicConfig(filename=setup.LOG_FILE,
                    level=setup.LOG_LEVEL,
                    format=setup.LOG_FORMAT,
                    datefmt=setup.LOG_DATE_FORMAT)


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        spider = js.JandanSpider()
        spider.start()
        logger.info("All task finished!")
    except BaseException as e:
        logger.error(e, exc_info=True)

