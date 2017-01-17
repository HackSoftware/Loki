from .services import get_snippets


class SnippetBasedView:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['snippets'] = get_snippets()

        return context
