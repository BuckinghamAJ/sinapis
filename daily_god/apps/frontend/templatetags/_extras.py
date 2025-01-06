from django import template
from taggit.models import TagBase, GenericTaggedItemBase
import logging
from frontend.functions import extract_text_between

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

    login_modal_html = f'''hx-get="{auth_url}"
            hx-push-url="false"
            hx-target="#login_modal"
            hx-trigger="click"
            hx-swap="innerHTML"'''

    if replacement_string:
        auth_button_html = button_html.replace(replacement_string, 
            login_modal_html)
    else:
        replacement_string = extract_text_between(button_html, 'auth_start', 'auth_end')
        log.debug(f"HTML: {button_html}")
        log.debug(replacement_string)
        auth_button_html = button_html.replace(replacement_string,
            login_modal_html)
    return auth_button_html

@register.tag(name="auth_button")
def do_login_auth_modal(parser, token):
    contents = token.split_contents()
    tag_name = contents[0]
    replacement_string = contents[1] if len(contents) > 1 else None
    nodelist = parser.parse(("endauth_button",))
    parser.delete_first_token()
    return LoginAuthModalNode(nodelist, replacement=replacement_string)

class LoginAuthModalNode(template.Node):
    def __init__(self, nodelist, replacement: str = None):
        self.nodelist = nodelist
        self.replacement = replacement[1:-1] if replacement else None
    
    def render(self, context):
        user = context['user']
        if user.is_authenticated:
            return self.nodelist.render(context).replace("auth_start", "").replace("auth_end", "")
        log.debug(str(self.replacement))
        return auth_button(self.nodelist.render(context), self.replacement)