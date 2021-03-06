from django.core.management.base import BaseCommand
from loki.hack_fmi.models import Room, Team


class Command(BaseCommand):
    help = 'distributes the teams in rooms'

    def handle(self, *args, **options):
        all_rooms = Room.objects.filter(season__is_active=True)

        teams_without_room = Team.objects.filter(season__is_active=True, room__isnull=True)

        free_capacity = sum([room.capacity for room in all_rooms if not room.is_full()])

        if len(teams_without_room) > free_capacity:
            error = "ERROR:   We have {} capacity and {} teams.".format(free_capacity, teams_without_room.count())
            print(error)
            notenough_capcity = len(teams_without_room) - free_capacity
            sorted_rooms = all_rooms.order_by('-capacity')

            while notenough_capcity > 0:
                for room in sorted_rooms:
                    if notenough_capcity > 0:
                        room.capacity += 1
                        room.save()
                        notenough_capcity -= 1
            all_rooms = sorted_rooms

        for team in teams_without_room:
            for room in all_rooms:
                if not room.is_full():
                    team.room = room
                    team.save()
                    continue
