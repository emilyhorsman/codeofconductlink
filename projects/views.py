from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView
from django.forms import models
from authentication.recaptcha import ReCAPTCHAField
from .models import Project

class ProjectList(ListView):
    model = Project
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.exclude(verified_date__isnull=True)

class ProjectDetail(DetailView):
    model = Project
    context_object_name = 'project'


class CreateProjectForm(models.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'homepage', 'tags',)

    recaptcha = ReCAPTCHAField(settings.RECAPTCHA_SECRET_KEY, settings.RECAPTCHA_SITE_KEY)

class CreateProject(CreateView):
    form_class = CreateProjectForm
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateProject, self).form_valid(form)
