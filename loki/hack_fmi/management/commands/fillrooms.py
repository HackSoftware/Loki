from django.core.management.base import BaseCommand
from hack_fmi.models import Room, Team


class Command(BaseCommand):
    help = 'distributes the teams in rooms'

    def handle(self, *args, **options):
        all_rooms = Room.objects.all()
        all_teams = Team.objects.all()
        all_teams = list(all_teams)
        while all_teams:
            for room in all_rooms:
                if not room.is_full():
                    current_team = all_teams.pop()
                    current_team.room = room
                    current_team.save()
