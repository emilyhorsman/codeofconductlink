from django import forms
from .models import SubmissionProfile

class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model  = SubmissionProfile
        fields = ('public_name',)
