import json
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from base_app.models import BaseUser, EducationInfo, EducationPlace, Faculty, Subject
from base_app.helper import get_or_none


INPUTS = {
    'text': forms.TextInput,
    'pass': forms.PasswordInput,
    'hidden': forms.HiddenInput
}


def w(input_type, value=None):
    element = INPUTS.get(input_type, None)

    if element is None:
        raise KeyError('{} not found as input type'.format(input_type))

    if value is None:
        return element()

    attrs = {'placeholder': value}
    return element(attrs=attrs)


class RegisterForm(forms.Form):
    first_name = forms.CharField(label=_('First Name'), widget=w('text', 'Име'))
    last_name = forms.CharField(label=_('Last Name'), widget=w('text', 'Фамилия'))
    email = forms.EmailField(widget=w('text', 'Email'))
    password = forms.CharField(label=_("Password"), widget=w('pass', 'Парола'))

    studies_at = forms.CharField(required=False)

    educationplace = forms.IntegerField(required=False, widget=w('hidden'))
    faculty = forms.IntegerField(required=False, widget=w('hidden'))
    subject = forms.IntegerField(required=False, widget=w('hidden'))

    start_date = forms.DateField(input_formats=['%d-%m-%Y'])
    end_date = forms.DateField(input_formats=['%d-%m-%Y'])

    def clean_password(self):
        password = self.cleaned_data.get("password")
        self._validate_password_strength(self.cleaned_data.get('password'))
        return password

    def clean(self):
        studies_at = self.cleaned_data.get('studies_at')
        educationplace_pk = self.cleaned_data.get('educationplace')
        faculty_pk = self.cleaned_data.get('faculty')
        subject_pk = self.cleaned_data.get('subject')

        if educationplace_pk is None and\
           faculty_pk is None and\
           subject_pk is None and\
           studies_at.strip() == "":
            raise ValidationError(_('Трябва да има дадено място за учене'))

        if educationplace_pk is not None:
            place = get_or_none(EducationPlace, pk=educationplace_pk)

            if place is None:
                raise ValidationError(_('Не намерихме това учебно заведение. Нещо се обърка?'))

            self.cleaned_data['educationplace'] = place

            if faculty_pk is not None:
                faculty = get_or_none(Faculty, pk=faculty_pk)

                if faculty is None:
                    raise ValidationError(_('Не намерихме този факултет. Нещо се обърка?'))

                self.cleaned_data['faculty'] = faculty

            if subject_pk is not None:
                subject = get_or_none(Subject, pk=subject_pk)

                if subject is None:
                    raise ValidationError(_('Не намерихме тази специалност. Нещо се обърка?'))

                self.cleaned_data['subject'] = subject

        return self.cleaned_data

    def save(self, commit=True):
        user = BaseUser.objects.create_user(
                email=self.cleaned_data.get('email'),
                password=self.cleaned_data.get('password'),
                full_name="{} {}".format(
                        self.cleaned_data.get('first_name'),
                        self.cleaned_data.get('last_name')))

        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        studies_at = self.cleaned_data.get('studies_at')

        educationplace = self.cleaned_data.get('educationplace')
        faculty = self.cleaned_data.get('faculty')
        subject = self.cleaned_data.get('subject')

        if educationplace is not None:
            info = EducationInfo(user=user, place=educationplace,
                                 start_date=start_date, end_date=end_date)

            if faculty is not None:
                info.faculty = faculty

            if subject is not None:
                info.subject = subject

            info.save()
        else:
            user.studies_at = studies_at.strip()
            user.save()

        return user

    def _validate_password_strength(self, value):
        """Validates that a password is as least 7 characters long and has at least
        1 digit and 1 letter.
        """
        min_length = 6

        if len(value) < min_length:
            raise ValidationError(_('Password must be at least {0} characters '
                                    'long.').format(min_length))

        # check for digit
        if not any(char.isdigit() for char in value):
            raise ValidationError(_('Password must container at least 1 digit.'))

        # check for letter
        if not any(char.isalpha() for char in value):
            raise ValidationError(_('Password must container at least 1 letter.'))


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'placeholder': 'Email adress', 'autofocus': ''}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
