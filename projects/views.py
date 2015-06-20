from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
from .forms import NewProjectForm
from .models import Project
from authentication.recaptcha import check_recaptcha

def index(request):
    projects = Project.objects.all()
    return render(request, 'projects/index.html', { 'projects': projects })

def detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/detail.html', { 'project': project })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            if settings.DEBUG or check_recaptcha(request):
                project = form.save(commit=False)
                project.user = request.user
                project.project = Project.objects.create(user=request.user)
                project.save()
                return redirect(reverse('projects:detail', args=(project.pk,)))
            else:
                form.add_error(None, 'You did not pass the reCAPTCHA.')
    else:
        form = NewProjectForm()
    return render(request, 'projects/new.html', { 'form': form, 'recaptcha': settings.RECAPTCHA_SITE_KEY })
