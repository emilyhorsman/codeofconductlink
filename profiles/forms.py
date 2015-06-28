from common.forms import create_crispy_model_form
from .models import Profile

class ProfileDetailForm(create_crispy_model_form(legend_text='Update Profile')):
    class Meta:
        model = Profile
        fields = ('public_name', 'profile_slug',)
