from django import template

register = template.Library()


@register.filter
def index(items, i):
    return items[int(i)]


@register.filter
def dict_index(items, key):
    return items[key]
