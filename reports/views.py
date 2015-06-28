from django.contrib.contenttypes.models import ContentType
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from vanilla import UpdateView, CreateView, DeleteView
from braces.views import UserPassesTestMixin, FormValidMessageMixin
from projects.models import Project
from common.access_mixins import VerifiedEmailRequiredMixin
from .models import Report
from .forms import CreateReportForm, UpdateReportForm
import projects.models

class DeleteReport(UserPassesTestMixin,
                   VerifiedEmailRequiredMixin,
                   DeleteView):
    model = Report

    def test_func(self, user):
        return Report.objects.filter(
                user=user,
                pk=self.request.resolver_match.kwargs['pk']
            ).exists()

    def no_permissions_fail(self, request):
        messages.error(request, 'You must own the report to delete it.')
        # This isn't the most ideal place to redirect to, but I don't really
        # care about the UX of a user that is likely malicious.
        return redirect(reverse('projects:index'))

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()

class CreateReport(FormValidMessageMixin,
                   VerifiedEmailRequiredMixin,
                   CreateView):
    model = Report
    form_valid_message = 'Report filed, thank you <3!'

    def get_target_object(self, request):
        return get_object_or_404(
                getattr(projects.models, self.request.GET['model']),
                pk=self.request.GET['pk'])

    def get_form(self, data=None, files=None, **kwargs):
        target = self.get_target_object(self.request)
        return CreateReportForm(data, files, target=target, **kwargs)

    def form_valid(self, form):
        target = self.get_target_object(self.request)
        form.instance.content_object = target
        form.instance.user = self.request.user
        self.success_url = target.get_absolute_url()
        return super(CreateReport, self).form_valid(form)

class UpdateReport(UserPassesTestMixin,
                   FormValidMessageMixin,
                   UpdateView):
    model = Report
    form_valid_message = 'Report updated.'

    def test_func(self, user):
        if not user.is_authenticated():
            return False

        if user.is_moderator:
            return True

        return Report.objects.filter(
                pk=self.request.resolver_match.kwargs['pk'],
                user=user
            ).exists()

    def no_permissions_fail(self, request):
        messages.error(request, 'You are not the owner of that report.')
        return redirect(reverse('projects:index'))

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()

    def get_form(self, data=None, files=None, **kwargs):
        return UpdateReportForm(data, files, request_user=self.request.user, **kwargs)
