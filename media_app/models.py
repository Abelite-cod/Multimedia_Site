from django.db import models
from django.contrib.auth.models import User
import os
from cloudinary.models import CloudinaryField



class UploadedFile(models.Model):
    FILE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('others', 'Others'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = CloudinaryField('file', folder='MultimediaSite/uploads')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='others')
    title = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.file_type})"

    def filename(self):
        return os.path.basename(self.file.url)
