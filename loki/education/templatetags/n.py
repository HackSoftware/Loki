from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def n(date_field):
    return date_field > timezone.now().date()
