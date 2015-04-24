from rest_framework.test import APITestCase
from .models import Season, Team, Mentor


class PlacerTests(APITestCase):
    def setUp(self):
        self.season = Season.objects.create(
            number=1,
            topic='TestTopic',
            is_active=True,
            sign_up_deadline="2015-5-1",
            mentor_pick_start_date="2015-4-1",
            mentor_pick_end_date="2015-5-1",
        )
        for i in range(1, 5):
            Team.objects.create(
                name='T{0}'.format(i),
                idea_description='GameDevelopers',
                repository='https://github.com/HackSoftware',
                season=self.season,
            )
        for i in range(1, 6):
            Mentor.objects.create(
                name='M{0}'.format(i),
                description='fancy mentor',
            )
        M1 = Mentor.objects.filter(name='M1').first()
        M2 = Mentor.objects.filter(name='M2').first()
        M3 = Mentor.objects.filter(name='M3').first()
        M4 = Mentor.objects.filter(name='M4').first()
        M5 = Mentor.objects.filter(name='M5').first()
        Team.objects.filter(name='T1').first().mentors.add(M1, M2, M3)
        Team.objects.filter(name='T2').first().mentors.add(M1, M2, M3, M4)
        Team.objects.filter(name='T3').first().mentors.add(M2, M3, M4)
        self.INPUT = [
            (team.name,
             [mentor.name for mentor in Team.objects.filter(name=team.name).first().mentors.all()])
            for team in Team.objects.all() if len(team.mentors.all()) != 0]

    def test_stuff(self):

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

        SLOTS = ["S{}".format(i) for i in range(1, 5)]


        INPUT = [(team.name,
                  [mentor.name for mentor in Team.objects.filter(name=team.name).first().mentors.all()])
                 for team in Team.objects.all() if len(team.mentors.all()) != 0]

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

        placing = attempt_placing(
            teams=teams_with_choice,
            mentors=chosen_mentors,
            slots=SLOTS,
            mentors_to_teams=mentors_to_teams)

        print(placing)
        print("Leftovers: ")
        print(placing["leftovers"])
