from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from base_app.models import BaseUser, EducationInfo, EducationPlace, Faculty, Subject
from base_app.helper import get_or_none, validate_password
from education.models import Student, Teacher, StudentAndTeacherCommonModel
from education.validators import validate_mac
from image_cropping import ImageCropWidget, ImageCropField
import re

INPUTS = {
    'text': forms.TextInput,
    'pass': forms.PasswordInput,
    'hidden': forms.HiddenInput
}

# w = widget
def w(input_type, value=None):
    element = INPUTS.get(input_type, None)

    if element is None:
        raise KeyError('{} not found as input type'.format(input_type))

    if value is None:
        return element()

    attrs = {'placeholder': value}
    return element(attrs=attrs)


class RegisterForm(forms.Form):
    first_name = forms.CharField(label=_('Име'), widget=w('text', 'Име'))
    last_name = forms.CharField(label=_('Фамилия'), widget=w('text', 'Фамилия'))
    email = forms.EmailField(widget=w('text', 'Email'))
    password = forms.CharField(label=_("Парола"), widget=w('pass', 'Парола'))

    def clean_password(self):
        password = self.cleaned_data.get("password")
        self._validate_password_strength(self.cleaned_data.get('password'))
        return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = get_or_none(BaseUser, email=email)
        if user is not None:
            raise ValidationError(_("Потребител с такъв email вече съществува"))

        return email

    def save(self, commit=True):
        user = BaseUser.objects.create_user(
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                email=self.cleaned_data.get('email'),
                password=self.cleaned_data.get('password'))
        user.save()
        return user

    def _validate_password_strength(self, value):
        validate_password(value)


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'placeholder': 'Email address', 'autofocus': ''}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class BaseEditForm(ModelForm):
    class Meta:
        model = BaseUser
        fields = ('first_name', 'last_name', 'full_image', 'cropping')

class StudentEditForm(ModelForm):
    class Meta:
        model = Student
        fields = ('mac', 'skype', 'phone')

class TeacherEditForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ('mac', 'phone', 'signature',)

class TeacherAndStudentEditForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ('signature',)
