from django.conf import settings
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from .recaptcha import ReCAPTCHAField
from .models import Profile

class ProfileDetail(UpdateView):
    model  = Profile
    fields = ('email', 'profile_name',)
    template_name = 'profiles/index.html'

    def get_object(self):
        return self.request.user

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileDetail, self).dispatch(*args, **kwargs)

class CreateProfileForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ('email', 'profile_name',)

    recaptcha = ReCAPTCHAField(settings.RECAPTCHA_SECRET_KEY, settings.RECAPTCHA_SITE_KEY)

class CreateProfile(CreateView):
    form_class = CreateProfileForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('profiles:detail')
