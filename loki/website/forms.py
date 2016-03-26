from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _
from base_app.models import BaseUser


class RegisterForm(forms.ModelForm):

    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput)

    class Meta:
        model = BaseUser
        fields = ("first_name", "last_name", "email", "studies_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': ''})

    def clean_password(self):
        password = self.cleaned_data.get("password")
        self._validate_password_strength(self.cleaned_data.get('password'))
        return password

    def save(self, commit=True):
        return BaseUser.objects.create_user(**self.cleaned_data)

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
        widget=forms.TextInput(attrs={'placeholder': 'Email adress'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
