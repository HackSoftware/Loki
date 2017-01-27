from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from loki.base_app.models import BaseUser
from loki.base_app.helper import get_or_none, validate_password
from loki.education.models import Student, Teacher, WorkingAt
from loki.education.validators import validate_phone, validate_github_account

INPUTS = {
    'text': forms.TextInput,
    'pass': forms.PasswordInput,
    'hidden': forms.HiddenInput,
    'checkbox': forms.CheckboxInput
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
        fields = ('first_name', 'last_name', 'github_account', 'full_image',
                  'cropping')
        labels = {
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'github_account': 'GitHub',
            'cropping': 'Изрежи снимката си'
        }

    def clean_github_account(self):
        github_account = self.cleaned_data.get("github_account").strip()
        validate_github_account(github_account)
        return github_account


class StudentEditForm(ModelForm):
    class Meta:
        model = Student
        fields = ('mac', 'skype', 'phone')

    def clean_phone(self):
        phone = self.cleaned_data.get("phone").strip()
        validate_phone(phone)
        return phone


class TeacherEditForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ('mac', 'phone', 'signature',)

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        validate_phone(phone)
        return phone


class WorkingAtForm(ModelForm):
    looking_for_job = forms.BooleanField(required=False, label="В момента работя, но си търся нова работа.")

    class Meta:
        model = WorkingAt
        fields = ("company", "start_date", "title", "description")

        labels = {
            'company': 'Компания',
            'start_date': 'Дата на започване',
            'title': 'Длъжност',
            'description': 'Описание'
        }

        widgets = {
            'start_date': w('text', 'yyyy-mm-dd')
        }
