from django import template

register = template.Library()
@register.filter(name='increment')

def increment(value):
    ret = int(value) + 1
    return str(ret)
