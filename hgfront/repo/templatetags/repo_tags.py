from django import template

register = template.Library()

@register.filter
def megs(value):
    size = (value/(1024*1024.0))
    return size