from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from allauth.account.decorators import verified_email_required
from .models import Project, Report
from .forms import CreateProjectForm

class ProjectIndex(ListView):
    context_object_name = 'projects'

    def get_queryset(self):
        # Only show projects that are
        # - verified
        # - not verified but the project's user is logged in
        # - not verified but a staff member/moderator is logged in
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
        context['report_text'] = self.object.report_text
        return context

class CreateProject(CreateView):
    form_class = CreateProjectForm
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Automatically verify projects submitted by staff.
        if form.instance.user.is_staff:
            form.instance.verify(form.instance.user, False)
        return super(CreateProject, self).form_valid(form)

    @method_decorator(verified_email_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateProject, self).dispatch(*args, **kwargs)

def can_verify(self):
    return self.request.user.is_moderator

@user_passes_test(can_verify)
def verify(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.verify(request.user)
    messages.success(request, '{} has been verified.'.format(project.name))
    return redirect(reverse('index'))
