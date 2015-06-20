from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import ProfileCreationForm, ProfileChangeForm

@login_required
def index(request):
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileChangeForm(instance=request.user)

    return render(request, 'profiles/index.html', { 'form': form })

def register(request):
    if request.user.is_authenticated():
        return redirect(reverse('profiles:index'))

    if request.method == 'POST':
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = ProfileCreationForm()
    return render(request, 'registration/register.html', { 'form': form })
