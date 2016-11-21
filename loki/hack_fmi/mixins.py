from .serializers import CompetitorInTeamSerializer, CustomTeamSerializer
from .models import TeamMembership


class MeSerializerMixin:

    def get(self, request, *args, **kwargs):
        competitor = self.request.user.get_competitor()

        data = {
            "is_competitor": bool(competitor),
            "competitor_info": None,
            "teams": None
        }
        if competitor:
            comp_inf = CompetitorInTeamSerializer(competitor)

            teams = TeamMembership.objects.list_all_teams_for_competitor(competitor=competitor)

            teams_data = None

            if teams:
                teams_data = CustomTeamSerializer(teams, many=True).data

            data["competitor_info"] = comp_inf.data
            data["teams"] = teams_data

        return data
