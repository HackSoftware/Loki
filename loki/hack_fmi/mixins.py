from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import CompetitorInTeamSerializer
from .permissions import IsJWTTokenBlackListed


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


class JwtApiAuthenticationMixin:
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsJWTTokenBlackListed, IsAuthenticated)
