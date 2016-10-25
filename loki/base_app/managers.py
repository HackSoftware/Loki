from django.contrib.auth.models import BaseUserManager
from django.apps import apps


class UserManager(BaseUserManager):

    def __create_user(self, email, password, full_name,
                      is_staff=False, is_active=False, is_superuser=False, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=is_active,
                          full_name=full_name,
                          is_superuser=is_superuser,
                          **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, full_name='', **kwargs):
        return self.__create_user(email, password, full_name, is_staff=False, is_active=False,
                                  is_superuser=False, **kwargs)

    def create_superuser(self, email, password, full_name=''):
        return self.__create_user(email, password, full_name, is_staff=True,
                                  is_active=True, is_superuser=True)

    def create(self, **kwargs):
        return self.create_user(**kwargs)

    def promote_to_student(self, user):
        Student = apps.get_model(app_label='education', model_name='Student')

        if not user.is_active:
            user.is_active = True
            user.save(using=self._db)

        student = Student(baseuser_ptr_id=user.id)
        student.__dict__.update(user.__dict__)

        """Will raise ValidationError if something's wrong"""
        student.full_clean()

        student.save(using=self._db)

        return Student.objects.get(pk=student.id)
