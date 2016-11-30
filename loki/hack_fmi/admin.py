from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from .models import (Competitor, Skill, Team, TeamMembership,
                     Invitation, Mentor, Season, Room, Partner,
                     TeamMentorship, BlackListToken)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Competitor)
class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'shirt_size')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'idea_description', 'room', 'season', 'get_members')

    list_filter = ('season',)

    def get_members(self, obj):
        return ", ".join([c.full_name for c in obj.members.all()])


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'competitor', 'team', 'is_leader')


@admin.register(TeamMentorship)
class TeamMentorshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'mentor', 'team')


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'competitor')


@admin.register(Mentor)
class MentorAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'from_company')


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'season', 'capacity')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(BlackListToken)
class BlackListTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'created_at')
