from import_export import resources
from .models import Student, CourseAssignment, WorkingAt


class StudentResource(resources.ModelResource):

    class Meta:
        model = Student


class CourseAssignmentResource(resources.ModelResource):

    class Meta:
        model = CourseAssignment


class WorkingAtResource(resources.ModelResource):

    class Meta:
        model = WorkingAt
        fields = (
            'student__email',
            'student__first_name',
            'student__last_name',
            'course',
            'came_working',
            'start_date',
            'title',
            'description',
            'company',
            'company_name'
        )
