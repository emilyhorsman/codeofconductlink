from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from .models import Project
from .forms import CreateProjectForm

class ProjectList(ListView):
    context_object_name = 'projects'

    def get_queryset(self):
        # Only show projects that are
        # - verified
        # - not verified but the project user is logged in
        # - not verified but the logged in user is staff/moderator
        u = self.request.user
        if u.is_authenticated() and u.can_verify:
            return Project.objects.all().order_by('verified_date')

        return Project.objects.filter(
            Q(verified_date__isnull=False) |
            Q(user=u.pk)
        ).order_by('verified_date')

class ProjectListByTag(ProjectList):
    def get_queryset(self):
        qs = super(ProjectListByTag, self).get_queryset()
        return qs.filter(tags__slug=self.kwargs['tag'])

class ProjectDetail(DetailView):
    model = Project
    context_object_name = 'project'

class CreateProject(CreateView):
    form_class = CreateProjectForm
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.user.is_staff:
            form.instance.verify(form.instance.user, False)
        return super(CreateProject, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateProject, self).dispatch(*args, **kwargs)

def can_verify(user):
    r = user.can_verify
    return r

@user_passes_test(can_verify)
def verify(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.verify(request.user)
    messages.success(request, '{} has been verified.'.format(project.name))
    return redirect(reverse('index'))
