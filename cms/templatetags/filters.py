from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name="truncate")
@stringfilter
def truncate(value, arg):
    return value[:int(arg)]

