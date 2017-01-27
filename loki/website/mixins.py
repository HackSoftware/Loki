from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import Http404

from .services import get_snippets


class AddSnippetsToContext:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['snippets'] = get_snippets()

        return context


class AddUserToContext:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user

        return context


class AnonymousRequired:
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(reverse('website:profile'))

        return super().dispatch(*args, **kwargs)


class CanAccessWorkingAtPermissionMisin:
    def dispatch(self, *args, **kwargs):
        if not self.request.user.get_student():
            raise Http404

        return super().dispatch(*args, **kwargs)
