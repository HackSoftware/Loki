import json
import os
from PIL.Image import Image
from loki.local_settings import MEDIA_ROOT


def crop_image(x1, y1, x2, y2, path):
    """ This is for the cropping of image """
    print(MEDIA_ROOT)
    print(path)
    # try:
    #     image = Image.open(os.path.join(BASE_DIR, path[1:]))
    # except IOError:
    #     return False
    # return image.crop(x1, y1, y2, x2)
