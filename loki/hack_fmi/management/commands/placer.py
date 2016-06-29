from django.core.management.base import BaseCommand
from hack_fmi.models import Team, Season
import json
from tabulate import tabulate


class Command(BaseCommand):
    help = 'places mentors in slots'

    def handle(self, *args, **options):

        def lowest_intersection(s1, s2):
            s1 = sorted(s1)
            s2 = sorted(s2)

            largest = s1
            smallest = s2

            if len(s2) > len(s1):
                largest = s2
                smallest = s1

            start = 0
            end = len(largest)

            while start < end:
                if largest[start] in smallest:
                    return largest[start]
                start += 1
            return None

        SLOTS = ["S{}".format(i) for i in range(1, 20)]

        season = Season.objects.filter(is_active=True)
        INPUT = [(team.name,
                  [mentor.name for mentor in Team.objects.filter(name=team.name).first().mentors.all()])
                 for team in Team.objects.filter(season=season) if len(team.mentors.all()) != 0]

        chosen_mentors = []
        teams_with_choice = []
        mentors_to_teams = {}

        for team, mentors in INPUT:
            if team not in teams_with_choice:
                teams_with_choice.append(team)

            for mentor in mentors:
                if mentor not in mentors_to_teams:
                    mentors_to_teams[mentor] = [team]
                else:
                    mentors_to_teams[mentor].append(team)

                if mentor not in chosen_mentors:
                    chosen_mentors.append(mentor)

        def attempt_placing(teams, mentors, slots, mentors_to_teams):

            mentor_slots_table = {mentor: slots[:] for mentor in mentors}
            team_slots_table = {team: slots[:] for team in teams}

            leftovers = []
            result = {}

            for mentor in chosen_mentors:
                teams = mentors_to_teams[mentor]

                for team in teams:
                    mentor_free_slots = mentor_slots_table[mentor]
                    team_free_slots = team_slots_table[team]

                    first_free_slot = lowest_intersection(mentor_free_slots, team_free_slots)
                    if first_free_slot is None:
                        leftovers.append((team, mentor))
                        continue

                    if mentor not in result:
                        result[mentor] = {}

                    result[mentor][first_free_slot] = team

                    if len(mentor_free_slots) != 0:
                        mentor_free_slots.remove(first_free_slot)

                    if len(team_free_slots) != 0:
                        team_free_slots.remove(first_free_slot)

            return {
                "placed": result,
                "leftovers": leftovers
            }

        def build_table_from_result(result, chosen_mentors):
            headers = ["Slots"] + chosen_mentors

            table = []

            for slot in SLOTS:
                teams_for_slot = []

                for mentor in chosen_mentors:
                    if slot in result[mentor]:
                        teams_for_slot.append(result[mentor][slot])
                    else:
                        teams_for_slot.append("EMPTY")

                table.append([slot] + teams_for_slot)

            return tabulate(table, headers=headers, tablefmt="fancy_grid")

        placing = attempt_placing(
            teams=teams_with_choice,
            mentors=chosen_mentors,
            slots=SLOTS,
            mentors_to_teams=mentors_to_teams)
        table = build_table_from_result(placing["placed"], chosen_mentors)

        json_placing = json.dumps(placing, indent=4)

        with open('media/placing.json', 'w') as f:
            f.write(json_placing)
            f.close()

        with open("media/mentors.html", "w") as f:
            f.write(table)
            f.close()
