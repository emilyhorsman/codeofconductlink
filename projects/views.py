from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
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
        if self.request.user.is_staff:
            return Project.objects.all().order_by('verified_date')

        return Project.objects.filter(
            Q(verified_date__isnull=False) |
            Q(user=self.request.user.pk)
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
