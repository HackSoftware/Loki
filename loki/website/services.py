from typing import Dict

from .models import Snippet


def get_snippets() -> Dict[str, Snippet]:
    return {snippet.label: snippet for snippet in Snippet.objects.all()}
