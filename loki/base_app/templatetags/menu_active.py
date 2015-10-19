import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def menu_active(context, pattern_or_urlname):
    try:
        # handle slash
        if reverse(pattern_or_urlname) == '/':
            pattern = '^/$'
        else:
            pattern = '^' + reverse(pattern_or_urlname) + "([-\w]+)?"
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''
