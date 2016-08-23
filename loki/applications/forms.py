from django import forms
from website.forms import w
from django.utils.translation import ugettext_lazy as _


class ApplyForm(forms.Form):
    phone = forms.CharField(label=_('Телефонен номер'), widget=w('text', 'Телефонен номер'))
    skype = forms.CharField(label=_('Skype'), widget=w('text', 'Skype'))
    works_at = forms.CharField(label=_('Къде работиш?'), widget=w('text', 'Къде работиш?'))
    studies_at = forms.CharField(label=_('Къде учиш?'), widget=w('text', 'Къде учиш?'))

    task_field_count = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        task_fields = kwargs.pop('tasks', 0)
        super(ApplyForm, self).__init__(*args, **kwargs)
        self.fields['task_field_count'].initial = task_fields
        for index in range(int(task_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['task_{index}'.format(index=index+1)] = \
                forms.URLField()
