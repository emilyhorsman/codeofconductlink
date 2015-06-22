from django.views.generic.edit import UpdateView
from braces.views import FormValidMessageMixin
from .access_mixins import VerifiedEmailRequiredMixin
from .models import Profile

class ProfileDetail(FormValidMessageMixin,
                    VerifiedEmailRequiredMixin,
                    UpdateView):
    model  = Profile
    fields = ('email', 'public_name', 'profile_slug',)
    template_name     = 'profiles/profile_detail.html'
    form_valid_message = 'Profile updated!'

    def get_object(self):
        return self.request.user
