from django.views.generic.edit import UpdateView
from braces.views import FormValidMessageMixin
from common.access_mixins import VerifiedEmailRequiredMixin
from .forms import ProfileDetailForm
from .models import Profile

class ProfileDetail(FormValidMessageMixin,
                    VerifiedEmailRequiredMixin,
                    UpdateView):
    model  = Profile
    template_name     = 'profiles/profile_detail.html'
    form_class = ProfileDetailForm
    form_valid_message = 'Profile updated!'

    def get_object(self):
        return self.request.user
