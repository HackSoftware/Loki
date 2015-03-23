from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class BaseUser(AbstractBaseUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    avatar = models.ImageField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password']


class Language(models.Model):
    name = models.CharField(max_length=30)


class Competitor(BaseUser):
    known_technologies = models.ManyToManyField(Language)
    faculty_number = models.SmallIntegerField()
