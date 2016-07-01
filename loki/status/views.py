from datetime import datetime
from rest_framework.decorators import api_view
# from rest_framework.decorators permission_classes
from rest_framework.response import Response

from education.models import CheckIn


@api_view(['GET'])
# @permission_classes((,))
def check_raspberry(request):
    date = datetime.now().date()
    if CheckIn.objects.filter(date=date).count():
        return Response(status=200)
    return Response(status=404)
