from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .recaptcha import ReCAPTCHAField
from .models import Profile

class CreateProfileForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ('email', 'profile_name',)

    def clean_profile_name(self):
        return self.cleaned_data.get('profile_name') or None

    recaptcha = ReCAPTCHAField()
