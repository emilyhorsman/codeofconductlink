from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile

class ProfileMeta(object):
    model  = Profile
    fields = ('email', 'profile_name')

class ProfileCreationForm(UserCreationForm):
    class Meta(ProfileMeta):
        pass

class ProfileChangeForm(forms.ModelForm):
    class Meta(ProfileMeta):
        pass
