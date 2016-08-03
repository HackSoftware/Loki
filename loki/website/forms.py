from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from base_app.models import BaseUser, EducationInfo, EducationPlace, Faculty, Subject
from base_app.helper import get_or_none, validate_password
from image_cropping import ImageCropWidget, ImageCropField

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

    # studies_at = forms.CharField(label=_(
    #     """Започни да пишеш и избери мястото, на което си учил от менюто.
    #     Ако не намираш мястото си - напиши града и пълното наименование и натисни
    #     'Не намирам моето' *"""), required=False)

    # educationplace = forms.IntegerField(required=False, widget=w('hidden'))
    # faculty = forms.IntegerField(required=False, widget=w('hidden'))
    # subject = forms.IntegerField(required=False, widget=w('hidden'))

    # start_date = forms.DateField(label=_('Дата на начало'), input_formats=['%d-%m-%Y'])
    # end_date = forms.DateField(label=_('Дата на край'), input_formats=['%d-%m-%Y'])
    # origin = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        self._validate_password_strength(self.cleaned_data.get('password'))
        return password

    # def clean(self):
    #     studies_at = self.cleaned_data.get('studies_at')
    #     educationplace_pk = self.cleaned_data.get('educationplace')
    #     faculty_pk = self.cleaned_data.get('faculty')
    #     subject_pk = self.cleaned_data.get('subject')
    #
    #     if educationplace_pk is None and\
    #        faculty_pk is None and\
    #        subject_pk is None and\
    #        studies_at.strip() == "":
    #         raise ValidationError(_('Трябва да има дадено място за учене'))
    #
    #     if educationplace_pk is not None:
    #         place = get_or_none(EducationPlace, pk=educationplace_pk)
    #
    #         if place is None:
    #             raise ValidationError(_('Не намерихме това учебно заведение. Нещо се обърка?'))
    #
    #         self.cleaned_data['educationplace'] = place
    #
    #         if faculty_pk is not None:
    #             faculty = get_or_none(Faculty, pk=faculty_pk)
    #
    #             if faculty is None:
    #                 raise ValidationError(_('Не намерихме този факултет. Нещо се обърка?'))
    #
    #             self.cleaned_data['faculty'] = faculty
    #
    #         if subject_pk is not None:
    #             subject = get_or_none(Subject, pk=subject_pk)
    #
    #             if subject is None:
    #                 raise ValidationError(_('Не намерихме тази специалност. Нещо се обърка?'))
    #
    #             self.cleaned_data['subject'] = subject
    #
    #     return self.cleaned_data

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

        # TODO: save start_date and end_date when the user hasnt selected educationplace
        # start_date = self.cleaned_data.get('start_date')
        # end_date = self.cleaned_data.get('end_date')
        # studies_at = self.cleaned_data.get('studies_at')
        #
        # educationplace = self.cleaned_data.get('educationplace')
        # faculty = self.cleaned_data.get('faculty')
        # subject = self.cleaned_data.get('subject')

        # if educationplace is not None:
        #     info = EducationInfo(user=user, place=educationplace,
        #                          start_date=start_date, end_date=end_date)
        #
        #     if faculty is not None:
        #         info.faculty = faculty
        #
        #     if subject is not None:
        #         info.subject = subject
        #
        #     info.save()
        # else:
        #     user.studies_at = studies_at.strip()

        user.save()
        return user

    def _validate_password_strength(self, value):
        validate_password(value)


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'placeholder': 'Email address', 'autofocus': ''}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class ProfileEditForm(ModelForm):
    class Meta:
        model = BaseUser
        fields = ('first_name', 'last_name', 'full_image', 'cropping')
