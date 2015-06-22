from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def icon(name, fallback='4x', css=''):
    s = settings.STATIC_URL
    css_classes = 'icon {}'.format(css).strip()
    return """<img class="icon {css_classes}" src="{s}open-iconic/svg/{name}.svg" onerror="this.src='{s}open-iconic/png/{name}-{fallback}.png'; this.onerror=null;" />""".format(s=s, name=name, css_classes=css_classes, fallback=fallback)
