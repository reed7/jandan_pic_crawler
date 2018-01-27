import logging
import time
import json

from selenium import webdriver, common
from bs4 import BeautifulSoup

from .setup import BEAUTIFUL_SOUP_BUILDER

logger = logging.getLogger(__name__)


def unicode_to_char(uni_str):
    if not uni_str:
        return ""

    try:
        str_ascii = ord(uni_str)
    except TypeError as te:
        logging.error(te.with_traceback())
        raise te

    return chr(str_ascii)


def parse_url_content_to_bs(url):
    co = webdriver.ChromeOptions()
    co.set_headless(True)
    driver = webdriver.Chrome(chrome_options=co)

    wait_sec = 2
    try:
        while True:
            try:
                driver.get(url)
                logger.debug("Page content reterived, converting to BS4 object!")
                ret = BeautifulSoup(driver.page_source, BEAUTIFUL_SOUP_BUILDER)
                return ret
            except common.exceptions.TimeoutException as te:
                if wait_sec > 2*2*2:
                    raise te

                logger.warning(
                    "Timeout during the process, retrying after {} seconds".format(wait_sec))
                time.sleep(wait_sec)
                wait_sec *= 2
                continue
    finally:
        driver.close()


class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
