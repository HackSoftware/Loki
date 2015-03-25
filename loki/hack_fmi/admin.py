from django.contrib import admin

from .models import Competitor, Skill


class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)

    class Meta:
        model = Skill


class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'shirt_size')

    class Meta:
        model = Competitor

admin.site.register(Skill, SkillAdmin)
admin.site.register(Competitor, CompetitorAdmin)
