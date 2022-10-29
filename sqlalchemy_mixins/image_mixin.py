import os

import sqlalchemy as sa


class ImageMixin:
    __abstract__ = True

    image = sa.Column(sa.String)

    @property
    def image_path(self):
        if self.image is None:
            return os.environ.get('APP_URL') + '/placeholder.png'
        return os.environ.get('CDN_URL') + self.image
