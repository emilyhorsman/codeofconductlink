from django import template
from urllib.parse import urlparse

def netloc(value):
    return '.'.join(urlparse(value).netloc.split('.')[-2:])

register = template.Library()
register.filter('netloc', netloc)
