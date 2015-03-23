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
    S = 1
    M = 2
    L = 3
    XL = 4

    SHIRT_SIZE = (
        (S, 'S'),
        (M, 'M'),
        (L, 'L'),
        (XL, 'XL')
    )

    known_technologies = models.ManyToManyField(Language)
    faculty_number = models.SmallIntegerField()
    shirt_size = models.SmallIntegerField(choices=SHIRT_SIZE, default=S)
