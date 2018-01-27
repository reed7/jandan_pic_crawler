import logging
import src.jandan_spider as js

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        spider = js.JandanSpider()
        spider.start()
        logger.info("All task finished!")
    except BaseException as e:
        logger.error(e, exc_info=True)

