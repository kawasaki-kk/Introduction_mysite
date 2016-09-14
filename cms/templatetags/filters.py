from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name="truncate")
@stringfilter
def truncate(value, arg):
    if int(len(value)) > int(arg):
        return value[:int(arg)] + ' ...'
    return value[:int(arg)]

