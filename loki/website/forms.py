import json
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from base_app.models import BaseUser, EducationInfo, EducationPlace, Faculty, Subject


class RegisterForm(forms.ModelForm):

    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(attrs={'placeholder': "Парола"}))
    education_info = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    start_date = forms.DateField(input_formats=['%d-%m-%Y'])
    end_date = forms.DateField(input_formats=['%d-%m-%Y'])

    class Meta:
        model = BaseUser
        fields = ("first_name", "last_name", "email", "password", "studies_at")

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': "Име", 'autofocus': ''}),
            'last_name': forms.TextInput(attrs={'placeholder': "Фамилия"}),
            'email': forms.EmailInput(attrs={'placeholder': "E-mail adress"}),
            'studies_at': forms.TextInput(attrs={'placeholder': "Образование"}),
            'education_info': forms.TextInput(),
            'start_date': forms.DateInput(),
            'end_date': forms.DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': ''})

    def clean_password(self):
        password = self.cleaned_data.get("password")
        self._validate_password_strength(self.cleaned_data.get('password'))
        return password

    def save(self, commit=True):
        user = BaseUser.objects.create_user(
                email=self.cleaned_data.get('email'),
                password=self.cleaned_data.get('password'),
                full_name="{} {}".format(
                        self.cleaned_data.get('first_name'),
                        self.cleaned_data.get('last_name')))

        education_info = json.loads(self.cleaned_data.get('education_info'))
        print(education_info)

        if 'other' in education_info:
            print('We have other')
            user.studies_at = education_info['other']
            user.save()

            return user

        education_place = EducationPlace.objects.get(pk=education_info['pk'])

        info = EducationInfo.objects.create(
                user=user,
                place=education_place,
                start_date=self.cleaned_data.get('start_date'),
                end_date=self.cleaned_data.get('end_date'))

        if 'faculty_pk' in education_info:
            faculty = Faculty.objects.get(pk=education_info['faculty_pk'])
            info.faculty = faculty

        if 'subject_pk' in education_info:
            subject = Subject.objects.get(pk=education_info['subject_pk'])
            info.subject = subject

        info.save()

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
