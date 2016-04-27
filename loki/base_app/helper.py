import os
from contextlib import contextmanager

from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


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


@contextmanager
def try_open(filename, mode="r"):
    try:
        f = open(filename, mode)
    except IOError as err:
        yield None, err
    else:
        try:
            yield f, None
        finally:
            f.close()


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def validate_password(value):
    """Validates that a password is as least 7 characters long and has at least
    1 digit and 1 letter.
    """

    min_length = 6

    if len(value) < min_length:
        raise ValidationError(_('Password must be at least {0} characters '
                                'long.').format(min_length))

    # check for digit
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('Password must container at least 1 digit.'))

    # check for letter
    if not any(char.isalpha() for char in value):
        raise ValidationError(_('Password must container at least 1 letter.'))


def split_and_lower(query):
    return [w.lower() for w in query.split()]
