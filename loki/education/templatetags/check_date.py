from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def is_date_in_future(date_field):
    return date_field > timezone.now().date()
