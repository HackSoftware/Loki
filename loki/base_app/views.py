from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib import messages

from .helper import validate_password
from .models import BaseUserRegisterToken, BaseUserPasswordResetToken, RegisterOrigin


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
