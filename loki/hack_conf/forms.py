from django.forms import ModelForm
from .models import HackConfUser


class HackConfUserForm(ModelForm):

    class Meta:
        model = HackConfUser
        fields = ['email']
