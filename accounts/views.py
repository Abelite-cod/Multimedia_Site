from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.models import User
from media_app.models import UploadedFile
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    # pass users to home template
    users = User.objects.all()
    return render(request, 'home.html', {'users': users})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    files = UploadedFile.objects.filter(user=user_obj).order_by('-uploaded_at')

    images = files.filter(file_type='image')
    videos = files.filter(file_type='video')
    audios = files.filter(file_type='audio')
    others = files.filter(file_type='others')

    context = {
        'profile_user': user_obj,
        'images': images,
        'videos': videos,
        'audios': audios,
        'others': others,
    }
    return render(request, 'accounts/profile.html', context)
