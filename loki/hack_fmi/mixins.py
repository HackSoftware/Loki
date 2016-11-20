from .serializers import CompetitorSerializer, CustomTeamSerializer
from .models import TeamMembership


class MeSerializerMixin:

    def get(self, request, *args, **kwargs):
        competitor = self.request.user.get_competitor()

        data = {
            "is_competitor": bool(competitor),
            "competitor_info": None,
            "team": None
        }
        if competitor:
            # TODO: Only `id`, `email`, `first_name` & `last_name` are needed. Create new serializer.
            comp_inf = CompetitorSerializer(competitor)

            teams = TeamMembership.objects.list_all_teams_for_competitor(competitor=competitor)

            teams_data = None

            if teams:
                teams_data = CustomTeamSerializer(teams, many=True).data

            data["competitor_info"] = comp_inf.data
            data["teams"] = teams_data

        return data
