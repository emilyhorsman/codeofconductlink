from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .recaptcha import ReCAPTCHAField
from .models import Profile

class CreateProfileForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ('email', 'profile_name',)

    recaptcha = ReCAPTCHAField()
