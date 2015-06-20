from django.conf import settings
import requests

def check_recaptcha(request):
    payload = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': request.POST.get('g-recaptcha-response')
    }
    res = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    res = res.json()
    return res['success']
