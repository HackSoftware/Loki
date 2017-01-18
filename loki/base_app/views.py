import json

from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib import messages

from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import BaseUserMeSerializer, UpdateBaseUserSerializer
from .helper import crop_image, validate_password
from .models import BaseUserRegisterToken, BaseUserPasswordResetToken, RegisterOrigin


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def me(request):
    logged_user = request.user
    serializer = BaseUserMeSerializer(logged_user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def baseuser_update(request):
    baseuser = request.user
    serializer = UpdateBaseUserSerializer(
        baseuser,
        data=request.data,
        partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=400)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def base_user_update(request):
    user = request.user
    co = request.data['selection']
    co = json.loads(co)

    data = {'full_image': request.data['file']}
    serializer = UpdateBaseUserSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        user = serializer.save()
        name = crop_image(int(co[0]), int(co[1]), int(co[3]), int(co[2]), str(user.full_image))
        user.avatar = name
        user.save()
        return Response(name, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=400)


def user_activation(request, token):
    token = get_object_or_404(BaseUserRegisterToken, token=token)
    user = token.user
    user.is_active = True
    user.save()
    token.delete()

    messages.success(request, 'Регистрацията ти е активирана успешно!')

    origin_name = request.GET.get('origin', None)
    origin = RegisterOrigin.objects.filter(name=origin_name).first()
    redirect_url = origin.redirect_url if origin else reverse('website:login')

    return redirect(redirect_url)


def user_password_reset(request, token):
    token = get_object_or_404(BaseUserPasswordResetToken, token=token)
    errors = []
    if request.POST and request.POST.get("password", False):
        user = token.user
        password = request.POST.get("password")
        try:
            validate_password(password)
        except ValidationError as e:
            errors = e
        else:
            user.set_password(password)
            user.save()
            token.delete()
            message = "Паролата ти беше успешно сменена!"

    return render(request, 'website/auth/password_reset.html', locals())
