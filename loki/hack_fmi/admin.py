from django.contrib import admin

from .models import Competitor, Skill, Team, TeamMembership, Invitation, Mentor, Season, Room, Partner


class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)

    class Meta:
        model = Skill


class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'shirt_size')

    class Meta:
        model = Competitor


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'idea_description', 'season')

    list_filter = ('season',)

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


class MentorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'from_company')

    class Meta:
        model = Mentor


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_active')

    class Meta:
        model = Season


class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'season', 'capacity')

    class Meta:
        model = Room


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name',)

    class Meta:
        model = Partner

admin.site.register(Team, TeamAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(TeamMembership, TeamMembershipAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Room, RoomAdmin)

