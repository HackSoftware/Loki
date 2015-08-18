from django.db import models


from ckeditor.fields import RichTextField


class Successor(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(blank=True)
    title = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ('order',)

    def __str__(self):
        return self.name


class SuccessViedeo(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True)
    youtube_link = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Snippet(models.Model):
    label = models.CharField(max_length=30, unique=True)
    text = RichTextField(blank=True)

    def __str__(self):
        return self.label
