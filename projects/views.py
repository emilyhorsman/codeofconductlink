from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View, ListView, DetailView, CreateView, FormView, UpdateView
from django.db.models import Q
from django.contrib import messages
from braces.views import UserPassesTestMixin
from common.access_mixins import VerifiedEmailRequiredMixin
from .models import Project, Report
from . import forms

class ProjectIndex(ListView):
    context_object_name = 'projects'

    def get_queryset(self):
        # Show all projects if a moderator is logged in. Otherwise only show
        # verified or owned projects.
        u = self.request.user
        if u.is_authenticated() and u.is_moderator:
            return Project.objects.all().order_by('verified_date')

        return Project.objects.filter(
            Q(verified_date__isnull=False) |
            Q(user=u.pk)
        ).order_by('verified_date')

class ProjectIndexByTag(ProjectIndex):
    def get_queryset(self):
        qs = super(ProjectIndexByTag, self).get_queryset()
        return qs.filter(tags__slug=self.kwargs['tag'])

class ProjectDetail(DetailView):
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['reports'] = self.object.get_reports_for_user(self.request.user)
        if self.object.user == self.request.user:
            context['can_edit'] = True

        return context

class ProjectOwnerPermissionsMixin(UserPassesTestMixin):
    permission_fail_message = 'You must be the project owner to perform the requested action.'

    def test_func(self, user):
        return Project.objects.filter(user=user,
                                      pk=self.request.resolver_match.kwargs['pk']).exists()

    def no_permissions_fail(self, request):
        messages.error(request, self.permission_fail_message)
        return redirect(reverse('projects:detail', args=(self.request.resolver_match.kwargs['pk'],)))


class ProjectUpdate(ProjectOwnerPermissionsMixin,
                    VerifiedEmailRequiredMixin,
                    UpdateView):
    model = Project
    form_class = forms.UpdateProjectForm
    template_name = 'projects/project_form.html'

class ProjectDelete(ProjectOwnerPermissionsMixin,
                    VerifiedEmailRequiredMixin,
                    CreateView):
    model = Project
    form_class = forms.DeleteProjectForm

class CreateProject(VerifiedEmailRequiredMixin, CreateView):
    form_class = forms.CreateProjectForm
    template_name = 'projects/project_form.html'

    # Automatically verify projects submitted by staff.
    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.user.is_staff:
            form.instance.verify(form.instance.user, False)
        return super(CreateProject, self).form_valid(form)

class ProjectVerify(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'])
        project.verify(request.user)
        messages.success(request, '{} has been verified.'.format(project.name))
        return redirect(reverse('projects:detail', args=(project.pk, project.name,)))

    def test_func(self, user):
        return user.is_moderator

    def no_permissions_fail(self, request):
        messages.error(request, 'You must be a moderator to verify this project.')
        return redirect(reverse('projects:detail', args=(self.request.resolver_match.kwargs['pk'],)))
