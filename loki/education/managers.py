from django.db import models


class StudentManager(models.Manager):
    def create_from_baseuser(self, baseuser):
        if baseuser.get_student() is not False:
            return None

        student = self.model(baseuser_ptr_id=baseuser.id)

        student.__dict__.update(baseuser.__dict__)
        student.save()

        return student
