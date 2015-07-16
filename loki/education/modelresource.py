from import_export import resources
from .models import Student, CourseAssignment


class StudentResource(resources.ModelResource):

    class Meta:
        model = Student


class CourseAssignmentResource(resources.ModelResource):

    class Meta:
        model = CourseAssignment
