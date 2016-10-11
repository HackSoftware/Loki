from django.template import Context, loader
from django.conf import settings


def render_template_with_context(target_html, context):
    """
    Receives:
      * `target_html` <string> - path from apps to the html file.
      * `context` <dict>

    Return `*.html`'s content, rendered with the given context.
    """
    path = settings.APPS_DIR + target_html
    template = loader.get_template(path)

    return template.render(Context(context))
