from import_export.admin import ImportExportActionModelAdmin

from django.contrib import admin

from base_app.models import BaseUser
from .models import (Company, Partner, City, GeneralPartner,
                     EducationPlace, University, Faculty, Subject, School, Academy, EducationInfo)


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'studies_at', 'works_at')

    list_filter = ('is_active',)
    search_fields = ['email', 'first_name', 'last_name', 'studies_at', 'works_at']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(GeneralPartner)


@admin.register(EducationPlace)
class EducationPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'city',
                    'is_uni', 'is_school', 'is_academy')


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'university')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty')


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')


@admin.register(Academy)
class AcademyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')


@admin.register(EducationInfo)
class EducationInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'faculty', 'subject')
