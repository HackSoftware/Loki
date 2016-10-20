from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from loki.education.models import Course

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
