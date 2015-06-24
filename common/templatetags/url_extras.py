from django import template
from urllib.parse import urlparse

register = template.Library()

@register.filter(name='netloc')
def netloc(value):
    return '.'.join(urlparse(value).netloc.split('.')[-2:])

@register.filter(name='truncatewith')
def truncatewith(text, args):
    length, replacement = args.split(",")
    length = int(length)
    if len(text) <= length:
        return text
    return replacement.strip()
