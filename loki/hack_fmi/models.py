from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def __create_user(self, email, password, is_admin,
                      first_name, last_name):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_admin=is_admin,
                          first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name='', last_name=''):
        return self.__create_user(email, password, False,
                                  first_name, last_name)

    def create_superuser(self, email, password, first_name='', last_name=''):
        return self.__create_user(email, password, True,
                                  first_name, last_name)


class BaseUser(AbstractBaseUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(blank=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_competitor(self):
        try:
            return self.competitor
        except:
            return False


class Language(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


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
