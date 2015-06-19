from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from projects.forms import ProfileRegistrationForm

def register(request):
    if request.method == 'POST':
        user_form    = UserCreationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user    = user_form.save()
            new_profile = profile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return redirect('/')
    else:
        user_form    = UserCreationForm()
        profile_form = ProfileRegistrationForm()
    return render(request, 'registration/register.html', { 'user_form': user_form, 'profile_form': profile_form })
