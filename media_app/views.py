from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadForm
from .models import UploadedFile

# expanded ext sets
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.heif'}
VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}
AUDIO_EXTS = {'.mp3', '.wav', '.ogg', '.m4a', '.flac'}

import os

def detect_file_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in IMAGE_EXTS:
        return 'image'
    if ext in VIDEO_EXTS:
        return 'video'
    if ext in AUDIO_EXTS:
        return 'audio'
    return 'others'


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.file_type = detect_file_type(upload.file.name)
            upload.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = UploadForm()
    return render(request, 'media_app/upload.html', {'form': form})


@login_required
def delete_file(request, pk):
    try:
        f = UploadedFile.objects.get(pk=pk, user=request.user)
        f.file.delete(save=False)
        f.delete()
    except UploadedFile.DoesNotExist:
        pass
    return redirect('user_profile', username=request.user.username)
