from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import RegisterForm, ProfileForm
from media_app.forms import UploadForm
from media_app.models import UploadedFile

import os

# Define file type sets
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.heif'}
VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}
AUDIO_EXTS = {'.mp3', '.wav', '.ogg', '.m4a', '.flac'}

def detect_file_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in IMAGE_EXTS:
        return 'image'
    if ext in VIDEO_EXTS:
        return 'video'
    if ext in AUDIO_EXTS:
        return 'audio'
    return 'others'

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
def home_view(request):
    users = User.objects.all()
    return render(request, 'home.html', {'users': users})

@login_required
def user_profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    files = UploadedFile.objects.filter(user=profile_user).order_by('-uploaded_at')

    upload_form = None
    profile_form = None

    if request.user == profile_user:
        if request.method == 'POST':
            if 'upload_file' in request.POST:
                upload_form = UploadForm(request.POST, request.FILES)
                if upload_form.is_valid():
                    upload = upload_form.save(commit=False)
                    upload.user = request.user
                    upload.file_type = detect_file_type(upload.file.name)
                    upload.save()
                    return redirect('user_profile', username=username)
            elif 'update_profile' in request.POST:
                profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
                if profile_form.is_valid():
                    profile_form.save()
                    return redirect('user_profile', username=username)
        else:
            upload_form = UploadForm()
            profile_form = ProfileForm(instance=request.user.profile)

    # Split files by type
    images = files.filter(file_type='image')
    videos = files.filter(file_type='video')
    audios = files.filter(file_type='audio')
    others = files.filter(file_type='others')

    context = {
        'profile_user': profile_user,
        'images': images,
        'videos': videos,
        'audios': audios,
        'others': others,
        'is_owner': request.user == profile_user,
        'upload_form': upload_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/profile.html', context)
