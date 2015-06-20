from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return redirect('/')

def register(request):
    return redirect('/')

"""
@login_required
def index(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.submissionprofile)
        #user_form = UserForm(request.POST, request.user)
        #user_form    = UserForm(user=request.user, data=request.POST)
        if profile_form.is_valid():
            profile_form.save()
        #if user_form.is_valid():
            #user_form.save()
    else:
        profile_form = ProfileForm(request.user.submissionprofile)
        #user_form    = UserForm(request.user)

    return render(request, 'profiles/index.html', { 'user_form': profile_form})
    #return render(request, 'profiles/index.html', { 'user_form': user_form, 'profile_form': profile_form })


def register(request):
    if request.method == 'POST':
        user_form    = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user    = user_form.save()
            new_profile = profile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return redirect('/')
    else:
        user_form    = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'registration/register.html', { 'user_form': user_form, 'profile_form': profile_form })
"""
