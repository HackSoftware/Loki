from django.contrib import admin

from .models import Competitor, Skill, Team, TeamMembership, Invitation


class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)

    class Meta:
        model = Skill


class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'shirt_size')

    class Meta:
        model = Competitor


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'idea_description')

    class Meta:
        model = Team


class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('competitor', 'team', 'is_leader')

    class Meta:
        model = TeamMembership


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('team', 'competitor')

    class Meta:
        model = Invitation

admin.site.register(Team, TeamAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(TeamMembership, TeamMembershipAdmin)
admin.site.register(Invitation, InvitationAdmin)
