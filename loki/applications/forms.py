from django import forms
# from django.core.exceptions import ValidationError
from base_app.models import BaseUser
from .models import (Application, ApplicationInfo,
                    ApplicationProblem, ApplicationProblemSolution)
from education.validators import validate_phone
from website.forms import w
from django.utils.translation import ugettext_lazy as _

class ApplyForm(forms.Form):
    phone = forms.CharField(label=_('Телефонен номер'), widget=w('text','Телефонен номер'))
    skype = forms.CharField(label=_('Skype'), widget=w('text','Skype'))
    works_at = forms.CharField(label=_('Къде работиш?'), widget=w('text','Къде работиш?'))
    studies_at = forms.CharField(label=_('Къде учиш?'), widget=w('text','Къде учиш?'))

    task_field_count = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        task_fields = kwargs.pop('tasks', 0)
        super(ApplyForm, self).__init__(*args, **kwargs)
        self.fields['task_field_count'].initial = task_fields
        for index in range(int(task_fields)):
           # generate extra fields in the number specified via extra_fields
            self.fields['task_{index}'.format(index=index+1)] = \
                forms.URLField()
    # def save(self, commit=True):
    #     user = BaseUser.objects.create_user(
    #             first_name=self.cleaned_data.get('first_name'),
    #             last_name=self.cleaned_data.get('last_name'),
    #             email=self.cleaned_data.get('email'),
    #             password=self.cleaned_data.get('password'))
    #     user.save()
    #     return user


# class RegisterForm(forms.Form):
#     first_name = forms.CharField(label=_('Име'), widget=w('text', 'Име'))
#     last_name = forms.CharField(label=_('Фамилия'), widget=w('text', 'Фамилия'))
#     email = forms.EmailField(widget=w('text', 'Email'))
#     password = forms.CharField(label=_("Парола"), widget=w('pass', 'Парола'))
#
#     def clean_password(self):
#         password = self.cleaned_data.get("password")
#         self._validate_password_strength(self.cleaned_data.get('password'))
#         return password
#
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         user = get_or_none(BaseUser, email=email)
#         if user is not None:
#             raise ValidationError(_("Потребител с такъв email вече съществува"))
#
#         return email
#
#     def save(self, commit=True):
#         user = BaseUser.objects.create_user(
#                 first_name=self.cleaned_data.get('first_name'),
#                 last_name=self.cleaned_data.get('last_name'),
#                 email=self.cleaned_data.get('email'),
#                 password=self.cleaned_data.get('password'))
#         user.save()
#         return user
#
#     def _validate_password_strength(self, value):
#         validate_password(value)
