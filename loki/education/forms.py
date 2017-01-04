import json

from django import forms
from loki.education.models import StudentNote


class FixJsonFieldDisplayInInheritedClassAdminForm(forms.ModelForm):
    """
    We have the following problem:

    If we create new test from some of the Test subclasses in the admin,
    the JSON gets stringified again.

    If we put { "foo": "bar" } we get "{\"foo\": \"bar\"}"

    This from does the following:

    1. Decodes once extra_options
    2. If, after the decoding, we have str, decode again
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.initial.get('extra_options') is None:
            return

        decoded = json.loads(self.initial['extra_options'])

        if isinstance(decoded, str):
            self.initial['extra_options'] = json.loads(self.initial['extra_options'])
