import logging
from multiprocessing import Pool, Process
from src.jandan_spider import Spider
from urllib import request

logger = logging.getLogger(__name__)
tucao_ids = [3673893, 3673885, 3673884]
tucao_url = "http://jandan.net/tucao/%d"

def get_tucao(tucao_id):
    print(tucao_id)
    url = tucao_url % tucao_id
    req = request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) "
                               "Chrome/63.0.3239.132 "
                               "Safari/537.36")
    with request.urlopen(req) as ret:
        print(ret.read())

if __name__ == "__main__":
    pool = Pool(8)
    pool.map(get_tucao, tucao_ids)
    """
    try:
        spider = Spider()
        spider.start()
    except BaseException as e:
        logger.error(e)
    """

