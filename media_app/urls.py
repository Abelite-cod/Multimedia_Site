from django.urls import path
from .views import upload_file, delete_file

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('delete/<int:pk>/', delete_file, name='delete_file'),
]
