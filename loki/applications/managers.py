from django.db import models


class ApplicationInfoManager(models.Manager):
    """
    TODO: Write tests
    """
    def get_open_for_apply(self):
        return [info for info in self.all() if info.apply_is_active()]
