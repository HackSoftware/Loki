from django.db import models


class ApplicationInfoManager(models.Manager):
    def get_open_for_apply(self):
        return [info for info in self.all() if info.apply_is_active()]
