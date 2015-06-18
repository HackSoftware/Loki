from import_export import resources
from .models import Student


class StudentResource(resources.ModelResource):

    class Meta:
        model = Student
