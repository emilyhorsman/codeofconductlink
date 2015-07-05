from django import template
from urllib.parse import urlparse

register = template.Library()

@register.simple_tag
def icon(css_class):
    base = '<i {} aria-hidden="true" role="presentation"></i>'
    if ';' in css_class:
        attrs = 'class="{}" data-hover="{}"'.format(*css_class.split(';'))
    else:
        attrs = 'class="{}"'.format(css_class)

    return base.format(attrs)
