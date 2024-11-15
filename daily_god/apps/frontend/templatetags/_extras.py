from django import template

register = template.Library()

@register.filter
def class_name(obj):
    print(obj.__class__.__name__)
    return obj.__class__.__name__