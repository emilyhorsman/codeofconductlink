from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView
from django.utils.decorators import method_decorator
from .models import Profile
from .forms import CreateProfileForm

class ProfileDetail(UpdateView):
    model  = Profile
    fields = ('email', 'profile_name',)
    template_name = 'profiles/index.html'

    def get_object(self):
        return self.request.user

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileDetail, self).dispatch(*args, **kwargs)

class CreateProfile(CreateView):
    form_class = CreateProfileForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('profiles:detail')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(reverse('index'))

        return super(CreateProfile, self).dispatch(*args, **kwargs)
