import os
from PIL import Image
from loki.local_settings import MEDIA_ROOT, MEDIA_URL


def crop_image(x1, y1, x2, y2, path):
    """ This is for the cropping of image """
    name = MEDIA_ROOT + 'avatar/' + 'cropped_' + path[2:]
    try:
        image = Image.open(os.path.join(MEDIA_ROOT, path[2:]))
    except IOError:
        return False
    img = image.crop((x1, y1, y2, x2))
    img.save(name)
    return MEDIA_URL + 'avatar/' + 'cropped_' + path[2:]
