from django import forms
from .models import SubmissionProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model  = SubmissionProfile
        fields = ('public_name',)
