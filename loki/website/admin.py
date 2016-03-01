from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import SuccessStoryPerson, SuccessVideo, Snippet, CourseDescription


class SuccessStoryPersonAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass
admin.site.register(SuccessStoryPerson, SuccessStoryPersonAdmin)


class SuccessVideoAdmin(admin.ModelAdmin):
    pass
admin.site.register(SuccessVideo, SuccessVideoAdmin)


class SnippetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Snippet, SnippetAdmin)


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

admin.site.register(CourseDescription, CourseDescriptionAdmin)
