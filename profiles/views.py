from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from allauth.account.decorators import verified_email_required
from .models import Profile

class ProfileDetail(UpdateView):
    model  = Profile
    fields = ('email', 'public_name', 'profile_slug',)
    template_name = 'profiles/profile_detail.html'

    def get_object(self):
        return self.request.user

    @method_decorator(verified_email_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileDetail, self).dispatch(*args, **kwargs)
