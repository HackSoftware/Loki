from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone

from loki.education.models import Course
from ..mixins import DashboardPermissionMixin

class CourseListView(DashboardPermissionMixin, ListView):
    model = Course

    def get_queryset(self):
        now = timezone.now().date()

        return Course.objects.filter(end_time__gte=now)
