from django import template
from urllib.parse import urlparse

register = template.Library()

@register.simple_tag
def icon(css_class):
    return """<i class="{}" aria-hidden="true" role="presentation"></i>""".format(css_class)
