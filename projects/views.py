from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.contrib import messages
from braces.views import UserPassesTestMixin
import vanilla
import reversion
from common.access_mixins import VerifiedEmailRequiredMixin
from .models import Project, Report, Submission, Vouch
from . import models
from . import forms

class ProjectIndex(vanilla.ListView):
    model = Project
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super(ProjectIndex, self).get_context_data(**kwargs)
        context['show_as_table'] = self.request.GET.get('format', '') == 'table'
        return context

    def get_queryset(self):
        return Project.index_qs_for_user(self.request.user)

class ProjectIndexByTag(ProjectIndex):
    def get_queryset(self):
        return Project.tag_qs_for_user(self.request.user, self.kwargs['tag'])

class ProjectDetail(vanilla.DetailView):
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)

        context['submissions'] = self.object.get_submissions_for_user(self.request.user)
        if self.request.user.is_authenticated():
            context['reports']     = self.object.get_reports_for_user(self.request.user)
            context['has_vouched'] = Vouch.has_vouched(self.object, self.request.user)
            context['can_edit']    = self.object.user == self.request.user or \
                                     self.request.user.is_moderator

        return context

class ProjectUpdatePermissionsMixin(UserPassesTestMixin):
    permission_fail_message = 'You must be the project owner to perform the requested action.'

    def test_func(self, user):
        if user.is_authenticated() and user.is_moderator:
            return True
        return Project.objects.filter(
                user=user,
                pk=self.request.resolver_match.kwargs['pk']
            ).exists()

    def no_permissions_fail(self, request):
        messages.error(request, self.permission_fail_message)
        return redirect(reverse('projects:detail', args=(self.request.resolver_match.kwargs['pk'],)))


class ProjectUpdate(ProjectUpdatePermissionsMixin,
                    VerifiedEmailRequiredMixin,
                    vanilla.UpdateView):
    model = Project
    form_class = forms.UpdateProjectForm

    @reversion.create_revision()
    def form_valid(self, form):
        return super(ProjectUpdate, self).form_valid(form)

class ProjectDelete(ProjectUpdatePermissionsMixin,
                    VerifiedEmailRequiredMixin,
                    vanilla.DeleteView):
    model = Project
    success_url = reverse_lazy('projects:index')

    @reversion.create_revision()
    def delete(self, request, *args, **kwargs):
        return super(ProjectDelete, self).delete(request, *args, **kwargs)

class CreateProject(VerifiedEmailRequiredMixin, vanilla.CreateView):
    model = Project
    form_class = forms.CreateProjectForm

    # Automatically verify projects submitted by staff.
    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.user.is_staff:
            form.instance.verify(form.instance.user, False)
        return super(CreateProject, self).form_valid(form)

def get_object_from_get_params(request):
    if request.GET.get('model', '') not in ['Project', 'Submission']:
        raise Http404()
    return get_object_or_404(
               getattr(models, request.GET.get('model')),
               pk=request.GET.get('pk'))

class ToggleVouch(VerifiedEmailRequiredMixin, vanilla.View):
    def post(self, request, *args, **kwargs):
        target = get_object_from_get_params(request)
        status = Vouch.toggle_vouch(target, request.user)
        messages.success(request, status)
        return redirect(target.get_absolute_url())

    def get(self, request, *args, **kwargs):
        target = get_object_from_get_params(request)
        return redirect(target.get_absolute_url())

class ToggleVerify(UserPassesTestMixin, vanilla.View):
    def post(self, request, *args, **kwargs):
        target = get_object_from_get_params(request)
        target.toggle_verify(request.user)
        return redirect(target.get_absolute_url())

    def get(self, request, *args, **kwargs):
        target = get_object_from_get_params(request)
        return redirect(target.get_absolute_url())

    def test_func(self, user):
        return user.is_authenticated() and user.is_moderator

    def no_permissions_fail(self, request):
        messages.error(request, 'You must be a moderator to verify data.')
        return redirect('/')

class SubmissionCreate(VerifiedEmailRequiredMixin, vanilla.CreateView):
    model = Submission

    def get_form(self, data=None, files=None, **kwargs):
        project = get_object_or_404(
                    Project,
                    pk=self.request.resolver_match.kwargs['project_pk'])
        return forms.CreateSubmissionForm(data=data, files=files, project=project, **kwargs)

    def form_valid(self, form):
        project = get_object_or_404(
                    Project,
                    pk=self.request.resolver_match.kwargs['project_pk'])
        form.instance.project = project
        form.instance.user = self.request.user
        self.success_url = project.get_absolute_url()
        return super(SubmissionCreate, self).form_valid(form)

class SubmissionUpdate(UserPassesTestMixin, vanilla.UpdateView):
    pass

class SubmissionDelete(UserPassesTestMixin, vanilla.DeleteView):
    pass
