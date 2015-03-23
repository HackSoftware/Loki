from django.contrib import admin

from .models import Competitor, Language


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)

    class Meta:
        model = Language


class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'shirt_size')

    class Meta:
        model = Competitor

admin.site.register(Language, LanguageAdmin)
admin.site.register(Competitor, CompetitorAdmin)
