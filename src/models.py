class PictureContainer(object):

    def __init__(self, id, like, dislike, img_src=None):
        self.id = id
        self.img_src = img_src
        self.like = like
        self.dislike = dislike

    def __str__(self):
        return "Picture info:[id={}, img_src={}, like/dislike={}/{}]".format(self.id,
                                                                             self.img_src,
                                                                             self.like,
                                                                             self.dislike)
