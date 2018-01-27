from multiprocessing import Process
from urllib import request
import json

from src.setup import *
from src.models import PictureTucao

logger = logging.getLogger(__name__)


class GetPicTucaoTaskRunner(Process):

    def __init__(self, pic_id, queue):
        Process.__init__(self)
        self.task_results = queue
        self.pic_id = pic_id

    def run(self):

        logger.info("Tucao grab task started! Pic_id: {}".format(self.pic_id))

        url = TUCAO_URL % self.pic_id
        logger.debug("Tucao URL: {}".format(url))

        req = request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/63.0.3239.132 "
                                     "Safari/537.36")

        with request.urlopen(req) as ret:
            ret = ret.read()

        self.task_results.put(_build_tucao_li(self.pic_id, json.loads(ret)))


def _build_tucao_li(pic_id, json_s):
    if not json_s:
        raise ValueError("The argument can't be empty!")

    logger.info("Building tucao list!")

    ret = []
    hot_tucao_li = json_s['hot_tucao']
    for ht in hot_tucao_li:
        tucao_model = _build_tucao(ht)
        ret.append(tucao_model)

    logger.info("Get {} hot tucaos for pic {}!".format(len(hot_tucao_li),
                                                       pic_id))
    return ret


def _build_tucao(json_s):
    if not json_s:
        logger.warning("The tucao JSON is empty, ignoring!")
        return

    comment_id = json_s["comment_ID"]
    logger.debug("Building tucao {}'s instance!".format(comment_id))

    pic_id = json_s["comment_post_ID"]
    author = json_s["comment_author"]
    date = json_s["comment_date"]
    content = json_s["comment_content"]
    parent = json_s["comment_parent"]
    like = json_s["vote_positive"]
    dislike = json_s["vote_negative"]

    return PictureTucao(comment_id, pic_id, author, content,
                       like, dislike, parent, date)