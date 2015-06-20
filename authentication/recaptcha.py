from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms.widgets import Widget
from django.forms.fields import Field
import requests

class ReCAPTCHAWidget(Widget):
    def render(self, name, value, attrs=None):
        return """<script src="https://www.google.com/recaptcha/api.js" async defer></script><div class="g-recaptcha" data-sitekey="{}"></div>""".format(settings.RECAPTCHA_SITE_KEY)

    def value_from_datadict(self, data, files, name):
        return data.get('g-recaptcha-response')

class ReCAPTCHAField(Field):
    default_error_messages = {
        'failed': 'Sorry, you did not pass the reCAPTCHA.'
    }

    widget = ReCAPTCHAWidget

    def __init__(self, secret_key, sitekey, *args, **kwargs):
        super(ReCAPTCHAField, self).__init__(*args, **kwargs)
        self.secret_key = secret_key
        self.sitekey = sitekey

    def to_python(self, value):
        return value

    def validate(self, value):
        payload = {
            'secret': self.secret_key,
            'response': value
        }
        res = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
        res = res.json()
        if not res['success']:
            raise ValidationError(self.error_messages['failed'], code='failed')
        return value
