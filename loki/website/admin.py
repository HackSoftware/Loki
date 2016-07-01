from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import (SuccessStoryPerson, SuccessVideo, Snippet,
                     CourseDescription)


@admin.register(SuccessStoryPerson)
class SuccessStoryPersonAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


@admin.register(SuccessVideo)
class SuccessVideoAdmin(admin.ModelAdmin):
    pass


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseDescription)
class CourseDescriptionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'course',
        'logo',
        'course_intensity',
        'course_days',
    ]

    list_filter = [
        'course_intensity',
        'course_days',
    ]

    search_fields = ['course']
