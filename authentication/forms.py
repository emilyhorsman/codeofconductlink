from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile

class ProfileCreationForm(UserCreationForm):
    class Meta:
        model  = Profile
        fields = ('email', 'profile_name')

class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ('email', 'profile_name')
