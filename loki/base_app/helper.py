import os
from PIL import Image
from django.conf import settings


def crop_image(x1, y1, x2, y2, path):
    size = (300, 300)
    name = settings.MEDIA_ROOT + 'avatar/' + 'cropped_' + path[2:]
    try:
        image = Image.open(os.path.join(settings.MEDIA_ROOT, path[2:]))
    except IOError:
        return False
    img = image.crop((x1, y1, y2, x2))
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(name)
    return settings.MEDIA_URL + 'avatar/' + 'cropped_' + path[2:]
