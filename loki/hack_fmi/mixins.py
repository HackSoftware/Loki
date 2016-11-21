from .serializers import CompetitorInTeamSerializer


class MeSerializerMixin:

    def get(self, request, *args, **kwargs):
        competitor = self.request.user.get_competitor()

        data = {
            "is_competitor": bool(competitor),
            "competitor_info": None
        }
        if competitor:
            comp_inf = CompetitorInTeamSerializer(competitor)

            data["competitor_info"] = comp_inf.data

        return data
