from django.contrib import admin

from .models import ApplyCourse

@admin.register(ApplyCourse)
class ApplyCourseAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'course',
    ]
