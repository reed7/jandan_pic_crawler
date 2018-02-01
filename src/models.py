from .utils import unicode_seq_to_str


class PictureContainer(object):

    def __init__(self, id, like, dislike, img_src=None):
        self.id = id
        self.img_src = img_src
        self.like = like
        self.dislike = dislike
        self.hot_tucao = None

    def __str__(self):
        return "Picture info:[id={}, img_src={}, like/dislike={}/{}]".format(self.id,
                                                                             self.img_src,
                                                                             self.like,
                                                                             self.dislike)


class PictureTucao(object):

    def __init__(self, id, pic_id, author, content, like, dislike,
                 parent=None, date=None):
        self.id = id
        self.pic_id = pic_id
        self.author = unicode_seq_to_str(author)
        self.date = date
        self.content = unicode_seq_to_str(content)
        self.parent = parent
        self.like = like
        self.dislike = dislike