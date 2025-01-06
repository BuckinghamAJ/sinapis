from django import template
from taggit.models import TagBase, GenericTaggedItemBase
import logging

log = logging.getLogger('app')
register = template.Library()

@register.filter
def class_name(obj):
    return obj.__class__.__name__

@register.filter
def check_tag(tag_name, obj):
    return tag_name in [tag.name for tag in obj.tags.all()]

def auth_button(button_html, replacement_string):
    from django.urls import reverse
    auth_url = reverse('profile_login')
    auth_button_html = button_html.replace(replacement_string, 
        f'''hx-get="{auth_url}"
        hx-push-url="false"
        hx-target="#login_modal"
        hx-trigger="click"
        hx-swap="innerHTML"''')
    return auth_button_html

@register.tag(name="auth_button")
def do_login_auth_modal(parser,token):
    tag_name, replacement_string = token.split_contents()
    nodelist = parser.parse(("endauth_button"),)
    parser.delete_first_token()
    return LoginAuthModalNode(nodelist, replacement=replacement_string)

class LoginAuthModalNode(template.Node):
    def __init__(self, nodelist, replacement: str = "auth_login"):
        self.nodelist = nodelist
        self.replacement = replacement.replace("'", "") 
    
    def render(self, context):
        user = context['user']
        if user.is_authenticated:
            return self.nodelist.render(context)
        log.debug(str(self.replacement))
        return auth_button(self.nodelist.render(context), self.replacement)