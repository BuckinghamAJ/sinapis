from django import template
from taggit.models import TagBase, GenericTaggedItemBase

register = template.Library()

@register.filter
def class_name(obj):
    return obj.__class__.__name__

@register.filter
def check_tag(tag_name, obj):
    return tag_name in [tag.name for tag in obj.tags.all()]