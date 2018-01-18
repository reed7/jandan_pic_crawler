from .models import PictureContainer


class PictureFilter(object):
    """ Determine if a picture meets the condition """

    def accept(self, pic_container):
        """Check the picture, subclass need to implement this function
        :param pic_container: a models.PictureContainer obj
        :return: bool """
        pass


class LikeDislikePictureFilter(PictureFilter):

    def accept(self, pic_container):
        if type(pic_container) is not PictureContainer:
            raise ValueError("Argument type need to be models.PictureContainer!!")

        like, dislike = pic_container.like, pic_container.dislike

        if like >= 50 and (like / dislike) >= 3:
            return True
        else:
            return False
