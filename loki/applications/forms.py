from django import forms
from loki.website.forms import w

from .models import Application, ApplicationProblemSolution

from django.utils.translation import ugettext_lazy as _


class ApplyForm(forms.Form):
    phone = forms.CharField(label=_('Телефонен номер'), widget=w('text', 'Телефонен номер'))
    skype = forms.CharField(label=_('Skype'), widget=w('text', 'Skype'))
    works_at = forms.CharField(label=_('Къде работиш?'), widget=w('text', 'Къде работиш?'))
    studies_at = forms.CharField(label=_('Къде учиш?'), widget=w('text', 'Къде учиш?'))

    task_field_count = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        app_problems = kwargs.pop('app_problems', 0)
        task_fields = kwargs.pop('tasks', 0)
        super(ApplyForm, self).__init__(*args, **kwargs)
        self.fields['task_field_count'].initial = task_fields
        """
        TODO: Consider rendering this in the HTML in the bright future
        """
        for index in range(int(task_fields)):
            task_label = '<a href={1} target="_blank">{2}</a> - задача {0}'.format(index+1,
                                                                                   app_problems[index].description_url,
                                                                                   app_problems[index].name)
            field = forms.URLField(label=task_label,
                                   widget=w('text', _('URL към gist със решение на задачата')))
            self.fields['task_{index}'.format(index=index + 1)] = field

    def save(self, app_info, app_problems, user):
        application = Application.objects.create(
            user=user,
            application_info=app_info,
            phone=self.cleaned_data.get('phone'),
            skype=self.cleaned_data.get('skype'),
            works_at=self.cleaned_data.get('works_at'),
            studies_at=self.cleaned_data.get('studies_at'))

        for index, app_problem in enumerate(app_problems):
            ApplicationProblemSolution.objects.create(
                application=application,
                problem=app_problem,
                solution_url=self.cleaned_data.get('task_{0}'.format(index+1))
            )

    def update(self, app_info, app_problems, user):
        application = Application.objects.get(user=user, application_info=app_info)
        application.phone = self.cleaned_data.get('phone')
        application.skype = self.cleaned_data.get('skype')
        application.works_at = self.cleaned_data.get('works_at')
        application.studies_at = self.cleaned_data.get('studies_at')
        application.save()

        for index, app_problem in enumerate(app_problems):
            solution = ApplicationProblemSolution.objects.get(application=application,
                                                              problem=app_problem)
            solution.solution_url = self.cleaned_data.get('task_{0}'.format(index+1))
            solution.save()
