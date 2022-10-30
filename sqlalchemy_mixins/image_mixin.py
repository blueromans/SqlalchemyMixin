import sqlalchemy as sa


class ImageMixin:
    __abstract__ = True
    __placeholder_path__ = ''
    __image_path__ = ''

    image = sa.Column(sa.String)

    @property
    def image_path(self):
        if self.image is None:
            return f'{self.__placeholder_path__}/placeholder.png'
        return self.__image_path__ + self.image
