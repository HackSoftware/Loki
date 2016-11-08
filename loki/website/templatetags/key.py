from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def key(d, key_name):
    if key_name in d:
        return d[key_name]
    else:
        None

key = register.filter('key', key)
