from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms.widgets import Widget
from django.forms.fields import Field
import requests

class ReCAPTCHAWidget(Widget):
    def render(self, name, value, attrs=None):
        if not settings.USE_RECAPTCHA:
            return 'reCAPTCHA is currently disabled.'
        return """<script src="https://www.google.com/recaptcha/api.js" async defer></script><div class="g-recaptcha" data-sitekey="{}"></div>""".format(settings.RECAPTCHA_SITE_KEY)

    def value_from_datadict(self, data, files, name):
        return data.get('g-recaptcha-response')

class ReCAPTCHAField(Field):
    default_error_messages = {
        'failed': 'Sorry, you did not pass the reCAPTCHA.'
    }

    widget = ReCAPTCHAWidget

    def to_python(self, value):
        return value

    def validate(self, value):
        if not settings.USE_RECAPTCHA:
            return True

        payload = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': value
        }
        res = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
        res = res.json()
        if not res['success']:
            raise ValidationError(self.error_messages['failed'], code='failed')
        return value
