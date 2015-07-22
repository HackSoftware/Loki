from django.db import models


class Successor(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(blank=True)
    title = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ('order',)

    def __str__(self):
        return self.name
