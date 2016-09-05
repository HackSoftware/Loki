from django.db import models


class StudentManager(models.Manager):
    def create_from_baseuser(self, baseuser):
        student = self.model(baseuser_ptr_id=baseuser.id)
        student.save()

        student.__dict__.update(baseuser.__dict__)
        return student.save()
